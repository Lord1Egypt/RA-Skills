#!/usr/bin/env python3
"""Channel- and cadence-neutral helpers for the concept-radar Skill."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

SCHEMA_VERSION = 1
API_VERSION = "2022-11-28"
OVERLAP_SECONDS = 300
MATURITY_LEVELS = {"hypothesis", "emerging", "growing", "established"}
CARD_TEXT_FIELDS = (
    "concept_name", "what", "why_important", "problem_solved",
    "compared_with", "similarities", "differences", "use_when",
    "not_replacement", "maturity", "action_recommendation",
)
EVIDENCE_FIELDS = {
    "what", "why_important", "problem_solved", "differences",
    "maturity", "action_recommendation",
}
ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CONFIG = ROOT / ".trae/concept-radar/authors.yaml"
DEFAULT_STATE = ROOT / ".trae/concept-radar/state.json"
DEFAULT_RUNTIME = ROOT / ".trae/concept-radar/runtime"


class RadarError(RuntimeError):
    pass


class RateLimitError(RadarError):
    def __init__(self, code, url):
        super().__init__(f"HTTP {code} rate limit for source")
        self.code, self.url = code, url


def utc_now():
    return dt.datetime.now(dt.timezone.utc).replace(
        microsecond=0
    ).isoformat().replace("+00:00", "Z")


def parse_time(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def content_hash(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def semantic_hash(text):
    normalized = re.sub(r"[^\w]+", "", (text or "").casefold(), flags=re.UNICODE)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def canonicalize_url(url):
    parsed = urllib.parse.urlsplit(url.strip())
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise RadarError("invalid source URL")
    path = re.sub(r"/+", "/", parsed.path or "/")
    query = urllib.parse.urlencode(sorted(
        urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    ))
    return urllib.parse.urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), path, query, "")
    )


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_state(path):
    try:
        state = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RadarError(f"state unreadable: {exc}") from exc
    if not isinstance(state, dict) or state.get("schema_version") != SCHEMA_VERSION:
        raise RadarError("unknown state schema")
    for key in ("sources", "items", "concepts"):
        if not isinstance(state.get(key), dict):
            raise RadarError(f"invalid state field: {key}")
    if state.get("pending_scan") is not None and not isinstance(
        state["pending_scan"], dict
    ):
        raise RadarError("invalid state field: pending_scan")
    return state


def _scalar(value):
    value = value.strip()
    if not value:
        return None
    if value.startswith("["):
        return json.loads(value.replace("'", '"'))
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value.isdigit():
        return int(value)
    if value in ("true", "false"):
        return value == "true"
    return value


def load_config(path):
    """Parse JSON or the intentionally small documented YAML subset."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {"selection": {}, "authors": []}
        current_author, section, source_kind = None, None, None
        for raw in text.splitlines():
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            indent, value = len(line) - len(line.lstrip()), line.strip()
            if indent == 0 and value.startswith("schema_version:"):
                data["schema_version"] = _scalar(value.split(":", 1)[1])
            elif indent == 0 and value == "selection:":
                section = "selection"
            elif indent == 0 and value == "authors:":
                section = "authors"
            elif section == "selection" and indent == 2:
                key, scalar = value.split(":", 1)
                data["selection"][key] = _scalar(scalar)
            elif section == "authors" and indent == 2 and value.startswith("- id:"):
                current_author = {
                    "id": _scalar(value.split(":", 1)[1]),
                    "topics": [],
                    "sources": {},
                }
                data["authors"].append(current_author)
                source_kind = None
            elif current_author is not None and indent == 4 and value.startswith("display_name:"):
                current_author["display_name"] = _scalar(value.split(":", 1)[1])
            elif current_author is not None and indent == 4 and value == "topics:":
                source_kind = "topics"
            elif current_author is not None and indent == 6 and source_kind == "topics" and value.startswith("- "):
                current_author["topics"].append(_scalar(value[2:]))
            elif current_author is not None and indent == 4 and value == "sources:":
                source_kind = None
            elif current_author is not None and indent == 6 and value.endswith(":"):
                source_kind = value[:-1]
                current_author["sources"][source_kind] = []
            elif current_author is not None and indent == 8 and value.startswith("- "):
                key, scalar = value[2:].split(":", 1)
                current_author["sources"][source_kind].append({key: _scalar(scalar)})
            elif current_author is not None and indent == 10 and ":" in value:
                key, scalar = value.split(":", 1)
                current_author["sources"][source_kind][-1][key] = _scalar(scalar)
    validate_config(data)
    return data


def validate_config(data):
    if data.get("schema_version") != SCHEMA_VERSION:
        raise RadarError("unknown config schema")
    selection = data.get("selection")
    if not isinstance(selection, dict) or not isinstance(
        selection.get("minimum_score"), int
    ):
        raise RadarError("invalid selection config")
    if not 1 <= selection.get("max_items_per_run", 0) <= 20:
        raise RadarError("max_items_per_run must be 1..20")
    authors = data.get("authors")
    if not isinstance(authors, list):
        raise RadarError("authors must be an array")
    identifiers = set()
    for author in authors:
        identifier = author.get("id")
        if (
            not isinstance(identifier, str)
            or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", identifier)
            or identifier in identifiers
        ):
            raise RadarError("author id must be stable and unique")
        identifiers.add(identifier)
        if not author.get("display_name") or not isinstance(author.get("topics"), list):
            raise RadarError(f"invalid author: {identifier}")
        for feed in author.get("sources", {}).get("feeds", []):
            canonicalize_url(feed["url"])
        for gist in author.get("sources", {}).get("gists", []):
            if not re.fullmatch(r"[A-Za-z0-9-]+", gist.get("username", "")):
                raise RadarError("invalid gist username")


def _is_rate_limit_error(exc, payload):
    headers = exc.headers or {}
    message = payload.decode("utf-8", errors="replace").lower()
    return exc.code == 429 or (
        exc.code == 403
        and (
            headers.get("x-ratelimit-remaining") == "0"
            or headers.get("Retry-After") is not None
            or "rate limit" in message
        )
    )


def request_bytes(url, headers=None, opener=None, retries=3):
    opener = opener or urllib.request.urlopen
    request = urllib.request.Request(url, headers=headers or {})
    delay = 0.05
    for attempt in range(retries):
        try:
            with opener(request, timeout=30) as response:
                return (
                    response.status,
                    dict(response.headers.items()),
                    response.read(),
                    response.geturl(),
                )
        except urllib.error.HTTPError as exc:
            if exc.code == 304:
                return 304, dict(exc.headers.items()), b"", url
            payload = exc.read()
            if not _is_rate_limit_error(exc, payload):
                raise RadarError(f"HTTP {exc.code} for source") from exc
            if attempt + 1 == retries:
                raise RateLimitError(exc.code, url) from exc
            time.sleep(delay)
            delay *= 2
        except urllib.error.URLError as exc:
            if attempt + 1 == retries:
                raise RadarError("source network failure") from exc
            time.sleep(delay)
            delay *= 2
    raise RadarError("unreachable")


def _header(headers, name):
    return next(
        (value for key, value in headers.items() if key.casefold() == name.casefold()),
        None,
    )


def _next_link(value):
    for part in (value or "").split(","):
        match = re.match(r'\s*<([^>]+)>;\s*rel="([^"]+)"', part)
        if match and match.group(2) == "next":
            return match.group(1)
    return None


class _PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.text, self._in_title, self._skip = "", [], False, 0

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag in ("script", "style", "noscript"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self._skip:
            value = re.sub(r"\s+", " ", data).strip()
            if value:
                self.text.append(value)


class _GistProfileParser(HTMLParser):
    def __init__(self, username, page_url):
        super().__init__(convert_charrefs=True)
        self.username, self.page_url = username, page_url
        self.gists, self.next_url = [], None

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        values = dict(attrs)
        href = values.get("href")
        if not href:
            return
        absolute = urllib.parse.urljoin(self.page_url, href)
        parsed = urllib.parse.urlsplit(absolute)
        parts = [urllib.parse.unquote(part) for part in parsed.path.split("/") if part]
        if (
            parsed.netloc.casefold() == "gist.github.com"
            and len(parts) == 2
            and parts[0].casefold() == self.username.casefold()
            and re.fullmatch(r"[0-9a-fA-F]+", parts[1])
        ):
            self.gists.append((parts[1], f"https://gist.github.com/{parts[0]}/{parts[1]}"))
        if "next" in {part.casefold() for part in values.get("rel", "").split()}:
            self.next_url = absolute


def scan_url(url, previous, opener=None):
    canonical = canonicalize_url(url)
    headers = {"Accept": "text/html,text/plain,application/xhtml+xml"}
    if previous.get("request_url") == canonical and previous.get("etag"):
        headers["If-None-Match"] = previous["etag"]
    status, response_headers, payload, final_url = request_bytes(
        canonical, headers, opener
    )
    if status == 304:
        return [], dict(previous)
    charset = "utf-8"
    content_type = _header(response_headers, "Content-Type") or ""
    match = re.search(r"charset=([\w-]+)", content_type, re.I)
    if match:
        charset = match.group(1)
    body = payload.decode(charset, errors="replace")
    title = canonical
    if "html" in content_type.casefold() or re.search(r"<html[\s>]", body[:1000], re.I):
        parser = _PageParser()
        parser.feed(body)
        title = re.sub(r"\s+", " ", parser.title).strip() or canonical
        body = "\n".join(parser.text)
    if not body.strip():
        raise RadarError("single URL returned no readable content")
    final = canonicalize_url(final_url)
    digest = content_hash(body)
    candidate = {
        "source_type": "url",
        "source_key": "url:" + final,
        "revision": _header(response_headers, "ETag")
        or _header(response_headers, "Last-Modified")
        or digest,
        "author_id": None,
        "author_name": urllib.parse.urlsplit(final).netloc,
        "title": title,
        "body": body,
        "published_at": None,
        "updated_at": None,
        "canonical_url": final,
        "content_hash": digest,
        "semantic_hash": semantic_hash(body),
    }
    return [candidate], {
        "cursor": None,
        "request_url": canonical,
        "etag": _header(response_headers, "ETag"),
        "last_modified": _header(response_headers, "Last-Modified"),
        "last_successful_scan_at": utc_now(),
        "transport": "single_url",
    }


def _xml_text(node):
    return "".join(node.itertext()).strip() if node is not None else ""


def parse_feed(payload, author, feed_url):
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise RadarError("invalid RSS/Atom XML") from exc
    rows = []
    if root.tag.lower().endswith("rss") or root.find("channel") is not None:
        for item in root.findall("./channel/item"):
            link = _xml_text(item.find("link"))
            canonical = canonicalize_url(link or feed_url)
            body = _xml_text(item.find("description"))
            published = _xml_text(item.find("pubDate")) or None
            rows.append((
                "rss:" + (_xml_text(item.find("guid")) or canonical),
                _xml_text(item.find("title")), body, published, canonical,
            ))
    else:
        namespace = {"a": "http://www.w3.org/2005/Atom"}
        for item in root.findall("a:entry", namespace) or root.findall("entry"):
            def find(name):
                namespaced = item.find("a:" + name, namespace)
                return namespaced if namespaced is not None else item.find(name)
            links = item.findall("a:link", namespace) or item.findall("link")
            href = next(
                (link.get("href") for link in links
                 if link.get("rel", "alternate") == "alternate"),
                feed_url,
            )
            canonical = canonicalize_url(href)
            body = _xml_text(find("content")) or _xml_text(find("summary"))
            published = _xml_text(find("updated")) or _xml_text(find("published")) or None
            rows.append((
                "atom:" + (_xml_text(find("id")) or canonical),
                _xml_text(find("title")), body, published, canonical,
            ))
    return [{
        "source_type": "feed",
        "source_key": key,
        "revision": published or content_hash(body),
        "author_id": author["id"],
        "author_name": author["display_name"],
        "title": title,
        "body": body,
        "published_at": published,
        "updated_at": published,
        "canonical_url": canonical,
        "content_hash": content_hash(body),
        "semantic_hash": semantic_hash(body),
    } for key, title, body, published, canonical in rows]


def scan_feed(author, source, previous, opener=None):
    url = canonicalize_url(source["url"])
    headers = {"Accept": "application/atom+xml,application/rss+xml,application/xml"}
    if previous.get("request_url") == url and previous.get("etag"):
        headers["If-None-Match"] = previous["etag"]
    status, response_headers, payload, final_url = request_bytes(url, headers, opener)
    if status == 304:
        return [], dict(previous)
    candidates = parse_feed(payload, author, final_url)
    newest = max(
        (item["updated_at"] for item in candidates if item["updated_at"]),
        default=previous.get("cursor"),
    )
    return candidates, {
        "cursor": newest,
        "request_url": url,
        "etag": _header(response_headers, "ETag"),
        "last_modified": _header(response_headers, "Last-Modified"),
        "last_successful_scan_at": utc_now(),
        "transport": "feed",
    }


def _scan_gists_profile(author, source, previous, opener=None):
    username = source["username"]
    first_url = f"https://gist.github.com/{urllib.parse.quote(username)}"
    url, visited, found = first_url, set(), []
    while url:
        page_key = canonicalize_url(url)
        if page_key in visited:
            raise RadarError("Gist profile pagination loop")
        parsed = urllib.parse.urlsplit(page_key)
        if (
            parsed.netloc != "gist.github.com"
            or parsed.path.rstrip("/").casefold() != f"/{username}".casefold()
        ):
            raise RadarError("unsafe Gist profile pagination URL")
        visited.add(page_key)
        status, _, payload, final_page_url = request_bytes(url, {}, opener)
        if status != 200:
            raise RadarError("cannot fetch Gist profile")
        parser = _GistProfileParser(username, final_page_url)
        parser.feed(payload.decode("utf-8"))
        found.extend(parser.gists)
        url = parser.next_url
    candidates, seen = [], set()
    for gist_id, canonical in found:
        if gist_id.casefold() in seen:
            continue
        seen.add(gist_id.casefold())
        raw_url = (
            "https://gist.githubusercontent.com/"
            f"{urllib.parse.quote(username)}/{urllib.parse.quote(gist_id)}/raw"
        )
        status, _, payload, final_raw_url = request_bytes(raw_url, {}, opener)
        if status != 200:
            raise RadarError("cannot fetch Gist raw content")
        body, final = payload.decode("utf-8"), canonicalize_url(final_raw_url)
        digest = content_hash(body)
        candidates.append({
            "source_type": "gist",
            "source_key": f"gist:{username}:{gist_id}",
            "revision": final if final != canonicalize_url(raw_url) else digest,
            "author_id": author["id"],
            "author_name": author["display_name"],
            "title": Path(urllib.parse.urlsplit(final_raw_url).path).name or f"Gist {gist_id}",
            "body": body,
            "published_at": None,
            "updated_at": None,
            "canonical_url": canonicalize_url(canonical),
            "content_hash": digest,
            "semantic_hash": semantic_hash(body),
        })
    return candidates, {
        "cursor": previous.get("cursor"),
        "request_url": canonicalize_url(first_url),
        "etag": None,
        "last_modified": None,
        "last_successful_scan_at": utc_now(),
        "transport": "gist_profile_raw",
    }


def _scan_gists_api(author, source, previous, opener=None):
    username = source["username"]
    params = {"per_page": "100"}
    cursor = previous.get("cursor")
    if cursor:
        since = parse_time(cursor) - dt.timedelta(seconds=OVERLAP_SECONDS)
        params["since"] = since.isoformat().replace("+00:00", "Z")
    url = (
        f"https://api.github.com/users/{urllib.parse.quote(username)}/gists?"
        + urllib.parse.urlencode(params)
    )
    request_key = canonicalize_url(url)
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": API_VERSION}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    if previous.get("request_url") == request_key and previous.get("etag"):
        headers["If-None-Match"] = previous["etag"]
    candidates, newest, response_meta = [], cursor, {}
    while url:
        status, response_headers, payload, _ = request_bytes(url, headers, opener)
        if status == 304:
            return [], dict(previous)
        try:
            rows = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise RadarError("invalid Gist JSON") from exc
        if not isinstance(rows, list):
            raise RadarError("invalid Gist response")
        response_meta = response_headers
        for gist in rows:
            files = gist.get("files", {})
            if gist.get("truncated") or any("content" not in info for info in files.values()):
                detail_url = gist.get("url")
                if not detail_url:
                    raise RadarError("Gist list item has no detail URL")
                detail_headers = {
                    key: value for key, value in headers.items()
                    if key.casefold() != "if-none-match"
                }
                detail_status, _, detail_payload, _ = request_bytes(
                    detail_url, detail_headers, opener
                )
                if detail_status != 200:
                    raise RadarError("cannot fetch Gist detail")
                try:
                    gist = json.loads(detail_payload)
                except json.JSONDecodeError as exc:
                    raise RadarError("invalid Gist detail JSON") from exc
                files = gist.get("files", {})
            chunks = []
            for info in files.values():
                body = info.get("content", "")
                if info.get("truncated"):
                    raw_url = info.get("raw_url")
                    if not raw_url:
                        raise RadarError("truncated Gist has no raw_url")
                    raw_status, _, raw, _ = request_bytes(raw_url, {}, opener)
                    if raw_status != 200:
                        raise RadarError("cannot complete truncated Gist")
                    body = raw.decode("utf-8")
                chunks.append(body)
            if not chunks:
                continue
            body = "\n\n".join(chunks)
            updated = gist.get("updated_at") or gist.get("created_at")
            candidates.append({
                "source_type": "gist",
                "source_key": f"gist:{username}:{gist['id']}",
                "revision": updated,
                "author_id": author["id"],
                "author_name": author["display_name"],
                "title": gist.get("description") or next(iter(files)),
                "body": body,
                "published_at": gist.get("created_at"),
                "updated_at": updated,
                "canonical_url": canonicalize_url(gist["html_url"]),
                "content_hash": content_hash(body),
                "semantic_hash": semantic_hash(body),
            })
            if updated and (not newest or parse_time(updated) > parse_time(newest)):
                newest = updated
        url = _next_link(_header(response_headers, "Link"))
        headers.pop("If-None-Match", None)
    return candidates, {
        "cursor": newest,
        "request_url": request_key,
        "etag": _header(response_meta, "ETag"),
        "last_modified": _header(response_meta, "Last-Modified"),
        "last_successful_scan_at": utc_now(),
        "transport": "github_api",
    }


def scan_gists(author, source, previous, opener=None):
    try:
        return _scan_gists_api(author, source, previous, opener)
    except RateLimitError as exc:
        is_api = urllib.parse.urlsplit(exc.url).netloc.casefold() == "api.github.com"
        if exc.code == 403 and is_api and not os.environ.get("GITHUB_TOKEN"):
            return _scan_gists_profile(author, source, previous, opener)
        raise


def is_seen(candidate, state):
    previous = state["items"].get(candidate["source_key"])
    if previous and (
        previous.get("revision") == candidate["revision"]
        or previous.get("content_hash") == candidate["content_hash"]
        or previous.get("semantic_hash") == candidate["semantic_hash"]
    ):
        return True
    return any(
        item.get("content_hash") == candidate["content_hash"]
        or item.get("semantic_hash") == candidate["semantic_hash"]
        for item in state["items"].values()
    )


def run_scan(mode="author-pool", url=None, config_path=DEFAULT_CONFIG,
             state_path=DEFAULT_STATE, runtime=DEFAULT_RUNTIME, opener=None):
    config, state = load_config(config_path), load_state(state_path)
    if state.get("pending_scan"):
        raise RadarError("pending_scan exists; validate or recover it before scanning")
    candidates, source_updates = [], {}
    if mode == "single-url":
        if not url:
            raise RadarError("single-url mode requires --url")
        key = "url:" + canonicalize_url(url)
        found, metadata = scan_url(url, state["sources"].get(key, {}), opener)
        candidates.extend(item for item in found if not is_seen(item, state))
        source_updates[key] = metadata
    elif mode == "author-pool":
        if url:
            raise RadarError("--url is only valid in single-url mode")
        if not config["authors"]:
            raise RadarError("author-pool mode requires at least one author")
        for author in config["authors"]:
            sources = author.get("sources", {})
            for gist in sources.get("gists", []):
                key = f"gists:{gist['username']}"
                found, metadata = scan_gists(
                    author, gist, state["sources"].get(key, {}), opener
                )
                candidates.extend(item for item in found if not is_seen(item, state))
                source_updates[key] = metadata
            for feed in sources.get("feeds", []):
                key = "feed:" + canonicalize_url(feed["url"])
                found, metadata = scan_feed(
                    author, feed, state["sources"].get(key, {}), opener
                )
                candidates.extend(item for item in found if not is_seen(item, state))
                source_updates[key] = metadata
    else:
        raise RadarError("unsupported scan mode")
    runtime = Path(runtime)
    runtime.mkdir(parents=True, exist_ok=True)
    atomic_json(runtime / "candidates.json", {
        "schema_version": SCHEMA_VERSION,
        "mode": mode,
        "candidates": candidates,
    })
    state["pending_scan"] = {
        "created_at": utc_now(),
        "mode": mode,
        "source_updates": source_updates,
        "candidate_meta": [{
            key: candidate[key] for key in (
                "source_key", "revision", "content_hash",
                "semantic_hash", "canonical_url",
            )
        } for candidate in candidates],
    }
    atomic_json(state_path, state)
    return candidates


def fingerprint(name):
    normalized = re.sub(r"[^\w]+", "", name.casefold(), flags=re.UNICODE)
    if not normalized:
        raise RadarError("empty concept name")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _score(item):
    scores = item.get("scores")
    if not isinstance(scores, dict):
        raise RadarError("scores must be an object")
    limits = {
        "novelty": (0, 3), "problem_clarity": (0, 2),
        "mechanism_clarity": (0, 2), "evidence_quality": (0, 2),
        "source_authority": (0, 1), "promotional_penalty": (-3, 0),
    }
    for key, (low, high) in limits.items():
        if not isinstance(scores.get(key), int) or not low <= scores[key] <= high:
            raise RadarError(f"invalid score: {key}")
    return sum(scores.values())


def _validate_sources_and_evidence(item, candidate):
    comparison_sources = item.get("comparison_sources")
    if not isinstance(comparison_sources, list) or not comparison_sources:
        raise RadarError("comparison_sources must be a non-empty array")
    allowed_urls = {candidate["canonical_url"]}
    for source in comparison_sources:
        if not isinstance(source, dict) or not isinstance(source.get("title"), str):
            raise RadarError("invalid comparison source")
        source_url = canonicalize_url(source.get("url", ""))
        source["url"] = source_url
        allowed_urls.add(source_url)
    evidence = item.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise RadarError("evidence must be a non-empty array")
    covered = set()
    for record in evidence:
        if not isinstance(record, dict):
            raise RadarError("invalid evidence record")
        field = record.get("field")
        if field not in CARD_TEXT_FIELDS:
            raise RadarError("evidence references an unknown field")
        if not isinstance(record.get("quote"), str) or not record["quote"].strip():
            raise RadarError("evidence quote must be non-empty")
        source_url = canonicalize_url(record.get("source_url", ""))
        if source_url not in allowed_urls:
            raise RadarError("evidence source is not declared")
        record["source_url"] = source_url
        covered.add(field)
    missing = EVIDENCE_FIELDS - covered
    if missing:
        raise RadarError("missing evidence for: " + ", ".join(sorted(missing)))


def render_digest(selected, candidate_map):
    blocks = []
    for item in selected:
        candidate = candidate_map[item["source_key"]]
        comparisons = "\n".join(
            f"- [{source['title']}]({source['url']})"
            for source in item["comparison_sources"]
        )
        evidence = "\n".join(
            f"- `{record['field']}`：{record['quote']}（[来源]({record['source_url']}））"
            for record in item["evidence"]
        )
        blocks.append(
            f"## 概念：{item['concept_name']}\n\n"
            f"**是什么**\n{item['what']}\n\n"
            f"**为什么重要**\n{item['why_important']}\n\n"
            f"**解决什么问题**\n{item['problem_solved']}\n\n"
            f"**成熟度与置信度**\n"
            f"- 成熟度：`{item['maturity']}`\n"
            f"- 置信度：{item['confidence']:.2f}\n\n"
            f"**和既有方案怎么比**\n"
            f"- 对比对象：{item['compared_with']}\n"
            f"- 相同点：{item['similarities']}\n"
            f"- 关键差异：{item['differences']}\n"
            f"- 更适合什么时候：{item['use_when']}\n"
            f"- 非替代边界：{item['not_replacement']}\n\n"
            f"**行动建议**\n{item['action_recommendation']}\n\n"
            f"**对比来源**\n{comparisons}\n\n"
            f"**证据**\n{evidence}\n\n"
            f"**主出处**\n[{candidate['author_name']}：{candidate['title']}]"
            f"({candidate['canonical_url']})"
        )
    return "\n\n---\n\n".join(blocks)


def validate_selection(selection_path, config_path=DEFAULT_CONFIG,
                       state_path=DEFAULT_STATE, runtime=DEFAULT_RUNTIME):
    config, state = load_config(config_path), load_state(state_path)
    if not state.get("pending_scan"):
        raise RadarError("no pending scan")
    runtime = Path(runtime)
    try:
        candidates_payload = json.loads(
            (runtime / "candidates.json").read_text(encoding="utf-8")
        )
        selection = json.loads(Path(selection_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RadarError(f"invalid runtime JSON: {exc}") from exc
    candidates = candidates_payload.get("candidates", [])
    candidate_map = {candidate["source_key"]: candidate for candidate in candidates}
    selected = selection.get("items") if isinstance(selection, dict) else selection
    if not isinstance(selected, list):
        raise RadarError("selection items must be an array")
    if len(selected) > config["selection"]["max_items_per_run"]:
        raise RadarError("too many selected items")
    seen_source, seen_revision, seen_hash, seen_fingerprint = set(), set(), set(), set()
    prepared = []
    for raw_item in selected:
        item = json.loads(json.dumps(raw_item))
        source_key = item.get("source_key")
        candidate = candidate_map.get(source_key)
        if not candidate or item.get("revision") != candidate["revision"]:
            raise RadarError("selection is not from current candidates")
        for field in CARD_TEXT_FIELDS:
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise RadarError(f"missing card field: {field}")
        if item["maturity"] not in MATURITY_LEVELS:
            raise RadarError("invalid maturity")
        confidence = item.get("confidence")
        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0 <= confidence <= 1
        ):
            raise RadarError("confidence must be between 0 and 1")
        if item.get("canonical_url") != candidate["canonical_url"]:
            raise RadarError("canonical URL mismatch")
        _validate_sources_and_evidence(item, candidate)
        total = _score(item)
        if (
            total < config["selection"]["minimum_score"]
            or item["scores"]["novelty"] == 0
            or item["scores"]["problem_clarity"] == 0
        ):
            raise RadarError("selection does not meet quality threshold")
        concept_fingerprint = fingerprint(item["concept_name"])
        keys = (
            source_key, candidate["revision"], candidate["content_hash"],
            concept_fingerprint,
        )
        if (
            keys[0] in seen_source or keys[1] in seen_revision
            or keys[2] in seen_hash or keys[3] in seen_fingerprint
        ):
            raise RadarError("duplicate within selection")
        if (
            concept_fingerprint in state["concepts"]
            and state["concepts"][concept_fingerprint].get("status") in (
                "exported", "published",
            )
        ):
            raise RadarError("concept was already exported")
        seen_source.add(keys[0])
        seen_revision.add(keys[1])
        seen_hash.add(keys[2])
        seen_fingerprint.add(keys[3])
        item["concept_fingerprint"] = concept_fingerprint
        item["total_score"] = total
        prepared.append(item)
    for candidate in candidates:
        picked = next(
            (item for item in prepared if item["source_key"] == candidate["source_key"]),
            None,
        )
        state["items"][candidate["source_key"]] = {
            "revision": candidate["revision"],
            "content_hash": candidate["content_hash"],
            "semantic_hash": candidate["semantic_hash"],
            "canonical_url": candidate["canonical_url"],
            "status": "exported" if picked else "rejected",
            "rejection_reason": None if picked else "not_selected",
            "concept_fingerprint": picked["concept_fingerprint"] if picked else None,
        }
        if picked:
            state["concepts"][picked["concept_fingerprint"]] = {
                "name": picked["concept_name"],
                "aliases": [],
                "preferred_source": candidate["source_key"],
                "status": "exported",
                "message_id": None,
            }
    state["sources"].update(state["pending_scan"]["source_updates"])
    state["pending_scan"] = None
    markdown = render_digest(prepared, candidate_map)
    output = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "items": prepared,
    }
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "concept-radar.md").write_text(markdown, encoding="utf-8")
    atomic_json(runtime / "concept-radar.json", output)
    atomic_json(state_path, state)
    (runtime / "candidates.json").unlink(missing_ok=True)
    return output, markdown


def parse_cli_json(completed, operation):
    if completed.returncode != 0:
        raise RadarError(f"{operation} failed with exit code {completed.returncode}")
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RadarError(f"{operation} returned invalid JSON") from exc
    if value.get("ok") is not True:
        raise RadarError(f"{operation} did not return ok=true")
    return value


def auth_status(runner=subprocess.run):
    completed = runner(
        ["lark-cli", "whoami", "--json"],
        capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0:
        raise RadarError(f"lark whoami failed with exit code {completed.returncode}")
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RadarError("lark whoami returned invalid JSON") from exc
    if value.get("identity") != "user" or value.get("available") is not True:
        raise RadarError("Feishu user identity is not available")
    if value.get("tokenStatus") not in (None, "ready"):
        raise RadarError("Feishu user token is not ready")
    open_id = value.get("onBehalfOf", {}).get("openId")
    if not open_id:
        raise RadarError("verified user openId missing")
    return open_id


def publish_feishu(state_path=DEFAULT_STATE, runtime=DEFAULT_RUNTIME,
                    runner=subprocess.run):
    state = load_state(state_path)
    output_path = Path(runtime) / "concept-radar.md"
    json_path = Path(runtime) / "concept-radar.json"
    if not output_path.exists() or not output_path.read_text(encoding="utf-8").strip():
        return None
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    unpublished = [
        item for item in payload["items"]
        if state["concepts"].get(item["concept_fingerprint"], {}).get("status") == "exported"
    ]
    if not unpublished:
        return None
    identity = "\n".join(sorted(
        f"{item['source_key']}@{item['revision']}" for item in unpublished
    ))
    idempotency_key = "cr-" + hashlib.sha256(identity.encode()).hexdigest()[:40]
    open_id = auth_status(runner)
    completed = runner([
        "lark-cli", "im", "+messages-send", "--user-id", open_id,
        "--markdown", output_path.read_text(encoding="utf-8"), "--as", "user",
        "--idempotency-key", idempotency_key,
    ], capture_output=True, text=True, check=False)
    response = parse_cli_json(completed, "lark message send")
    message_id = response.get("message_id") or response.get("data", {}).get("message_id")
    if not message_id:
        raise RadarError("successful response has no message_id")
    for item in unpublished:
        fingerprint_value = item["concept_fingerprint"]
        state["concepts"][fingerprint_value]["status"] = "published"
        state["concepts"][fingerprint_value]["message_id"] = message_id
        state["items"][item["source_key"]]["status"] = "published"
    atomic_json(state_path, state)
    return message_id


def run_doctor(config_path=DEFAULT_CONFIG, state_path=DEFAULT_STATE,
               channel=None, runner=subprocess.run):
    checks = {}
    try:
        load_config(config_path)
        checks["config"] = "ok"
    except Exception as exc:
        checks["config"] = str(exc)
    try:
        load_state(state_path)
        checks["state"] = "ok"
    except Exception as exc:
        checks["state"] = str(exc)
    checks["python"] = "ok" if sys.version_info >= (3, 9) else "Python 3.9+ required"
    if channel is None:
        checks["publishing"] = "not requested"
    elif channel == "feishu":
        checks["lark_cli"] = "ok" if shutil.which("lark-cli") else "missing"
        if checks["lark_cli"] == "ok":
            try:
                auth_status(runner)
                checks["feishu_user"] = "ok"
            except Exception as exc:
                checks["feishu_user"] = str(exc)
        else:
            checks["feishu_user"] = "not checked"
    else:
        raise RadarError("unsupported channel")
    return checks


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--state", default=str(DEFAULT_STATE))
    parser.add_argument("--runtime", default=str(DEFAULT_RUNTIME))
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("scan")
    scan.add_argument("--mode", choices=("author-pool", "single-url"))
    scan.add_argument("--url")
    validate = commands.add_parser("validate-selection")
    validate.add_argument("--selection", required=True)
    publish = commands.add_parser("publish")
    publish.add_argument("--channel", choices=("feishu",), required=True)
    doctor = commands.add_parser("doctor")
    doctor.add_argument("--channel", choices=("feishu",))
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            mode = args.mode or ("single-url" if args.url else "author-pool")
            result = {"candidates": run_scan(
                mode, args.url, args.config, args.state, args.runtime
            )}
        elif args.command == "validate-selection":
            output, markdown = validate_selection(
                args.selection, args.config, args.state, args.runtime
            )
            result = {"json": output, "markdown": markdown}
        elif args.command == "publish":
            result = {"message_id": publish_feishu(args.state, args.runtime)}
        else:
            result = run_doctor(args.config, args.state, args.channel)
        print(json.dumps({"ok": True, "result": result}, ensure_ascii=False))
        return 0
    except RadarError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
