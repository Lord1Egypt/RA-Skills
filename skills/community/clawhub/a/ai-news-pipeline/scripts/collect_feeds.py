from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


BASE_DIR = Path(os.getenv("AI_NEWS_WORKSPACE", os.getcwd())).resolve()
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "sources.json"
DEFAULT_INTERNATIONAL_CONFIG_PATH = BASE_DIR / "config" / "international_sources.json"
LEGACY_INTERNATIONAL_CONFIG_PATH = BASE_DIR / "international_sources.json"
STATE_PATH = BASE_DIR / "state" / "feed_state.json"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
USER_AGENT = "AINewsCollect/1.0 (+rss-collector)"
MAX_SEEN_IDS_PER_SOURCE = 5000

INTERNATIONAL_DATA_PREFIX = "international"
INTERNATIONAL_TOPICS = [
    "llm",
    "foundation model",
    "foundation models",
    "model",
    "models",
    "agent",
    "agents",
    "ai",
    "artificial intelligence",
    "generative ai",
    "genai",
    "multimodal",
    "reasoning model",
    "reasoning models",
]
INTERNATIONAL_EVENTS = [
    "guideline",
    "guidelines",
    "funding",
    "fundraise",
    "fundraising",
    "raise",
    "raises",
    "raised",
    "investment",
    "invest",
    "invests",
    "acquisition",
    "acquire",
    "acquires",
    "acquired",
    "launch",
    "launches",
    "launched",
    "release",
    "releases",
    "released",
    "approval",
    "approved",
    "policy",
    "regulation",
    "regulatory",
    "partnership",
    "partner",
    "partners",
    "deal",
]
AI_SCOPED_SOURCE_HINTS = [
    "artificial-intelligence",
    "artificialintelligence",
    "/ai/",
    "ai-techpark",
    "venturebeat.com/category/ai",
]

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
CONTENT_NAMESPACES = [
    "{http://purl.org/rss/1.0/modules/content/}encoded",
    "{http://www.w3.org/2005/Atom}content",
    "{http://www.w3.org/2005/Atom}summary",
]


@dataclass
class SourceConfig:
    name: str
    url: str
    enabled: bool = True
    headers: dict[str, str] | None = None
    username: str | None = None
    password: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect new entries from RSS/Atom feeds.")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to the domestic sources config file. Default: {DEFAULT_CONFIG_PATH}",
    )
    parser.add_argument(
        "--international-config",
        type=Path,
        default=DEFAULT_INTERNATIONAL_CONFIG_PATH,
        help=(
            "Path to the international sources config file. "
            f"Default: {DEFAULT_INTERNATIONAL_CONFIG_PATH}"
        ),
    )
    return parser.parse_args()


def configure_output_encoding() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def ensure_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_INTERNATIONAL_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_sources(config_path: Path, *, required: bool) -> list[SourceConfig]:
    path = config_path
    if not path.exists():
        if path == DEFAULT_INTERNATIONAL_CONFIG_PATH and LEGACY_INTERNATIONAL_CONFIG_PATH.exists():
            path = LEGACY_INTERNATIONAL_CONFIG_PATH
        elif required:
            raise FileNotFoundError(f"Config file not found: {path}")
        else:
            return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{path.name} must be a JSON array of source objects.")

    sources: list[SourceConfig] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Source #{index} in {path.name} must be an object.")

        name = str(item.get("name", "")).strip()
        url = str(item.get("url", "")).strip()
        if not name or not url:
            raise ValueError(f"Source #{index} in {path.name} is missing name or url.")

        sources.append(
            SourceConfig(
                name=name,
                url=url,
                enabled=bool(item.get("enabled", True)),
                headers=dict(item.get("headers") or {}),
                username=item.get("username"),
                password=item.get("password"),
            )
        )

    return [source for source in sources if source.enabled]


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"sources": {}, "international_sources": {}}

    with STATE_PATH.open("r", encoding="utf-8") as file:
        state = json.load(file)

    if not isinstance(state, dict):
        return {"sources": {}, "international_sources": {}}

    state.setdefault("sources", {})
    state.setdefault("international_sources", {})
    return state


def save_state(state: dict[str, Any]) -> None:
    with STATE_PATH.open("w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)


def append_failure_log(message: str, *, source_name: str | None = None) -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"{today}.log"
    timestamp = datetime.now().astimezone().isoformat()
    prefix = f"[{timestamp}]"
    if source_name:
        prefix = f"{prefix} [{source_name}]"

    with log_path.open("a", encoding="utf-8") as file:
        file.write(f"{prefix} {message}\n")

    return log_path


def build_request(source: SourceConfig) -> Request:
    headers = {"User-Agent": USER_AGENT}
    if source.headers:
        headers.update(source.headers)

    if source.username and source.password:
        basic_token = base64.b64encode(f"{source.username}:{source.password}".encode("utf-8")).decode("ascii")
        headers["Authorization"] = f"Basic {basic_token}"

    return Request(source.url, headers=headers)


def fetch_feed(source: SourceConfig) -> bytes:
    request = build_request(source)
    with urlopen(request, timeout=30) as response:
        return response.read()


def extract_text(element: ET.Element | None, *tags: str) -> str:
    if element is None:
        return ""

    for tag in tags:
        child = element.find(tag, ATOM_NS)
        if child is not None and child.text:
            return child.text.strip()
    return ""


def extract_content(element: ET.Element) -> str:
    description = extract_text(element, "description", "atom:summary")
    if description:
        return description

    for tag in CONTENT_NAMESPACES:
        child = element.find(tag)
        if child is not None:
            text = "".join(child.itertext()).strip()
            if text:
                return text
    return ""


def extract_link(element: ET.Element) -> str:
    link_text = extract_text(element, "link")
    if link_text:
        return link_text

    for link_element in element.findall("atom:link", ATOM_NS):
        href = link_element.attrib.get("href", "").strip()
        rel = link_element.attrib.get("rel", "alternate").strip()
        if href and rel in {"", "alternate"}:
            return href
    return ""


def normalize_datetime(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        return ""

    try:
        return parsedate_to_datetime(cleaned).isoformat()
    except (TypeError, ValueError, IndexError, OverflowError):
        pass

    try:
        return datetime.fromisoformat(cleaned.replace("Z", "+00:00")).isoformat()
    except ValueError:
        return cleaned


def build_item_id(source_name: str, guid: str, link: str, title: str, published_at: str, content: str) -> str:
    raw = "||".join([source_name, guid, link, title, published_at, content])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def parse_rss_item(item: ET.Element, source: SourceConfig) -> dict[str, str]:
    title = extract_text(item, "title")
    guid = extract_text(item, "guid")
    link = extract_link(item)
    published_at = normalize_datetime(extract_text(item, "pubDate"))
    content = extract_content(item)
    return {
        "source_name": source.name,
        "source_url": source.url,
        "title": title,
        "content": content,
        "published_at": published_at,
        "link": link,
        "guid": guid,
        "item_id": build_item_id(source.name, guid, link, title, published_at, content),
    }


def parse_atom_entry(entry: ET.Element, source: SourceConfig) -> dict[str, str]:
    title = extract_text(entry, "atom:title")
    guid = extract_text(entry, "atom:id")
    link = extract_link(entry)
    published_at = normalize_datetime(extract_text(entry, "atom:published", "atom:updated"))
    content = extract_content(entry)
    return {
        "source_name": source.name,
        "source_url": source.url,
        "title": title,
        "content": content,
        "published_at": published_at,
        "link": link,
        "guid": guid,
        "item_id": build_item_id(source.name, guid, link, title, published_at, content),
    }


def parse_feed(content: bytes, source: SourceConfig) -> list[dict[str, str]]:
    root = ET.fromstring(content)

    items = root.findall("./channel/item")
    if not items and root.tag.endswith("RDF"):
        items = root.findall("./item")
    if items:
        return [parse_rss_item(item, source) for item in items]

    entries = root.findall("./atom:entry", ATOM_NS)
    if entries:
        return [parse_atom_entry(entry, source) for entry in entries]

    raise ValueError(f"Unrecognized RSS/Atom format for {source.name}")


def append_records(records: list[dict[str, Any]], *, prefix: str | None = None) -> Path | None:
    if not records:
        return None

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}.jsonl" if prefix is None else f"{prefix}_{today}.jsonl"
    output_path = DATA_DIR / filename

    with output_path.open("a", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
    return output_path


def deduplicate_new_items(state: dict[str, Any], source: SourceConfig, items: list[dict[str, str]], *, state_key: str) -> list[dict[str, Any]]:
    source_state = state[state_key].setdefault(source.name, {"seen_ids": []})
    seen_ids = set(source_state.get("seen_ids", []))
    new_records: list[dict[str, Any]] = []

    for item in items:
        item_id = item["item_id"]
        if item_id in seen_ids:
            continue

        record = {
            "captured_at": datetime.now().astimezone().isoformat(),
            "source_name": item["source_name"],
            "source_url": item["source_url"],
            "title": item["title"],
            "content": item["content"],
            "published_at": item["published_at"],
            "link": item["link"],
            "guid": item["guid"],
        }
        new_records.append(record)
        source_state.setdefault("seen_ids", []).append(item_id)

    source_state["seen_ids"] = source_state.get("seen_ids", [])[-MAX_SEEN_IDS_PER_SOURCE:]
    source_state["last_checked_at"] = datetime.now().astimezone().isoformat()
    return new_records


def normalize_match_text(*values: str) -> str:
    return " ".join(value.lower() for value in values if value).strip()


def count_keyword_hits(match_text: str, keywords: list[str]) -> int:
    return sum(1 for keyword in keywords if keyword in match_text)


def is_ai_scoped_source(source: SourceConfig) -> bool:
    scope_text = normalize_match_text(source.name, source.url)
    return any(hint in scope_text for hint in AI_SCOPED_SOURCE_HINTS)


def is_relevant_international_item(item: dict[str, str], source: SourceConfig) -> bool:
    match_text = normalize_match_text(item.get("title", ""), item.get("content", ""), item.get("link", ""))
    if not match_text:
        return False

    topic_hits = count_keyword_hits(match_text, INTERNATIONAL_TOPICS)
    event_hits = count_keyword_hits(match_text, INTERNATIONAL_EVENTS)
    if event_hits == 0:
        return False

    if is_ai_scoped_source(source):
        return True
    return topic_hits > 0


def collect_source_group(
    sources: list[SourceConfig],
    state: dict[str, Any],
    *,
    state_key: str,
    label: str,
    output_prefix: str | None,
    filter_relevant: bool,
) -> tuple[int, int, Path | None]:
    all_new_records: list[dict[str, Any]] = []
    error_count = 0

    if not sources:
        return 0, 0, None

    for source in sources:
        try:
            raw_feed = fetch_feed(source)
            items = parse_feed(raw_feed, source)
            filtered_items = [item for item in items if is_relevant_international_item(item, source)] if filter_relevant else items
            new_records = deduplicate_new_items(state, source, filtered_items, state_key=state_key)
            all_new_records.extend(new_records)

            if filter_relevant:
                print(f"[OK] {label} {source.name}: fetched {len(items)}, matched {len(filtered_items)}, new {len(new_records)}")
            else:
                print(f"[OK] {label} {source.name}: fetched {len(items)}, new {len(new_records)}")
        except FileNotFoundError:
            raise
        except HTTPError as error:
            error_count += 1
            message = f"{label} HTTP ERROR: {error.code} {error.reason}"
            print(f"[HTTP ERROR] {label} {source.name}: {error.code} {error.reason}", file=sys.stderr)
            append_failure_log(message, source_name=source.name)
        except URLError as error:
            error_count += 1
            message = f"{label} URL ERROR: {error.reason}"
            print(f"[URL ERROR] {label} {source.name}: {error.reason}", file=sys.stderr)
            append_failure_log(message, source_name=source.name)
        except ET.ParseError as error:
            error_count += 1
            message = f"{label} PARSE ERROR: {error}"
            print(f"[PARSE ERROR] {label} {source.name}: {error}", file=sys.stderr)
            append_failure_log(message, source_name=source.name)
        except Exception as error:
            error_count += 1
            message = f"{label} ERROR: {error}"
            print(f"[ERROR] {label} {source.name}: {error}", file=sys.stderr)
            append_failure_log(message, source_name=source.name)

    output_path = append_records(all_new_records, prefix=output_prefix)
    if output_path:
        print(f"Wrote {len(all_new_records)} new {label} records to {output_path}")
    else:
        print(f"No new {label} records this run")

    if error_count:
        append_failure_log(
            f"{label} run completed with {len(all_new_records)} new records and {error_count} failing sources."
        )

    return len(all_new_records), error_count, output_path


def collect_once(config_path: Path, international_config_path: Path) -> int:
    ensure_directories()
    domestic_sources = load_sources(config_path, required=True)
    international_sources = load_sources(international_config_path, required=False)
    state = load_state()

    if not domestic_sources and not international_sources:
        print("No enabled RSS sources found. Fill config/sources.json or config/international_sources.json first.")
        return 0

    domestic_count, _, _ = collect_source_group(
        domestic_sources,
        state,
        state_key="sources",
        label="domestic",
        output_prefix=None,
        filter_relevant=False,
    )
    international_count, _, _ = collect_source_group(
        international_sources,
        state,
        state_key="international_sources",
        label="international",
        output_prefix=INTERNATIONAL_DATA_PREFIX,
        filter_relevant=True,
    )

    save_state(state)
    total_new_records = domestic_count + international_count
    print(f"Total new records this run: {total_new_records}")
    return total_new_records


def main() -> int:
    configure_output_encoding()
    args = parse_args()
    try:
        collect_once(args.config.resolve(), args.international_config.resolve())
        return 0
    except Exception as error:
        print(f"Run failed: {error}", file=sys.stderr)
        append_failure_log(f"Run failed: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
