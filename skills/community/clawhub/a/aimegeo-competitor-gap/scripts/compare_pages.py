#!/usr/bin/env python3
"""Extract comparable page evidence; narrative recommendations belong to the agent."""

import argparse
import copy
import csv
import hashlib
import json
import re
import sys
from datetime import datetime
from http.client import HTTPException, IncompleteRead
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


LIMIT = 3 * 1024 * 1024
CRAWLERS = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]
SAMPLE_STATES = {"observed", "simulated", "not_run", "query_failed"}


class InputError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InputError(message)


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def checked_url(value):
    require(text_value(value), "URL must be a nonempty string")
    try:
        parts = urlsplit(value)
        require(parts.scheme in {"http", "https"} and parts.hostname
                and not parts.username and not parts.password, "Expected HTTP(S) URL without credentials")
        _ = parts.port
    except ValueError as exc:
        raise InputError(f"Invalid URL: {value}") from exc
    return urlunsplit((parts.scheme, parts.netloc, parts.path or "/", parts.query, ""))


def timestamp(value):
    try:
        require(text_value(value), "captured_at is required")
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(parsed.tzinfo is not None, "captured_at must include timezone")
    except (TypeError, ValueError) as exc:
        raise InputError("captured_at must be an ISO-8601 timestamp with timezone") from exc


def validate(data):
    require(isinstance(data, dict), "Input must be a JSON object")
    scope = data.get("comparison", {})
    require(isinstance(scope, dict) and text_value(scope.get("question")), "comparison.question is required")
    slots = scope.get("page_slots")
    require(isinstance(slots, list) and slots and all(text_value(s) for s in slots)
            and len(slots) == len(set(slots)), "page_slots must contain unique nonempty names")
    sites = data.get("sites")
    require(isinstance(sites, list) and len(sites) >= 2, "Supply one brand and at least one competitor")
    ids, resources = set(), {}
    for site in sites:
        require(isinstance(site, dict), "Each site must be an object")
        require(text_value(site.get("id")) and site["id"] not in ids, "Site ids must be unique")
        ids.add(site["id"])
        require(text_value(site.get("name")), "Site name is required")
        require(isinstance(site.get("role"), str) and site["role"] in {"brand", "competitor"},
                "Invalid site role")
        require(isinstance(site.get("aliases", []), list)
                and all(text_value(a) for a in site.get("aliases", [])), "aliases must be nonempty strings")
        pages = site.get("pages", [])
        require(isinstance(pages, list), "pages must be an array")
        seen_slots = set()
        for page in pages:
            require(isinstance(page, dict) and page.get("slot") in slots
                    and page["slot"] not in seen_slots, "Each page needs a unique declared slot")
            seen_slots.add(page["slot"])
        items = pages + ([site["robots"]] if "robots" in site else [])
        for item in items:
            require(isinstance(item, dict), "Resource must be an object")
            url = checked_url(item.get("url"))
            snap = item.get("snapshot")
            if snap is not None:
                require(isinstance(snap, dict), "snapshot must be an object")
                require(isinstance(snap.get("status"), str) and snap["status"] in {"ok", "failed", "not_run"},
                        "Invalid snapshot status")
                require(isinstance(snap.get("kind"), str) and snap["kind"] in {"observed", "simulated"},
                        "snapshot.kind is required")
                timestamp(snap.get("captured_at"))
                if snap["status"] == "ok":
                    require(text_value(snap.get("path")), "Successful snapshot needs path")
                    require(type(snap.get("http_status")) is int and 200 <= snap["http_status"] < 300,
                            "Successful snapshot needs a 2xx http_status")
                else:
                    require(text_value(snap.get("reason")), "Non-successful snapshot needs reason")
                if "final_url" in snap:
                    checked_url(snap["final_url"])
            signature = json.dumps(snap, sort_keys=True, ensure_ascii=False)
            require(url not in resources or resources[url] == signature,
                    "Same URL has conflicting acquisition records; use one capture per run")
            resources[url] = signature
    require(sum(s["role"] == "brand" for s in sites) == 1, "Exactly one brand is required")
    samples = data.get("ai_samples", [])
    require(isinstance(samples, list), "ai_samples must be an array")
    sample_ids = set()
    for sample in samples:
        require(isinstance(sample, dict) and text_value(sample.get("id"))
                and sample["id"] not in sample_ids, "AI sample ids must be unique")
        sample_ids.add(sample["id"])
        require(isinstance(sample.get("status"), str) and sample["status"] in SAMPLE_STATES,
                "Invalid AI sample status")
        require(text_value(sample.get("platform")) and text_value(sample.get("query")),
                "AI sample needs platform and query")
        if sample["status"] in {"observed", "simulated"}:
            timestamp(sample.get("captured_at"))
            require(text_value(sample.get("answer")) and text_value(sample.get("evidence")),
                    "Completed AI sample needs answer and evidence reference")
            require("native_citations" in sample, "Use null for uncollected native citations, [] for observed none")
            citations = sample["native_citations"]
            require(citations is None or isinstance(citations, list), "native_citations must be null or array")
            for citation in citations or []:
                require(isinstance(citation, dict), "Citation must be an object")
                checked_url(citation.get("url"))
        else:
            require(text_value(sample.get("reason")), "Failed/unrun AI sample needs reason")
            require(not sample.get("answer") and sample.get("native_citations") is None,
                    "Failed/unrun samples cannot carry completed answers or citation counts")
    return data


class Loader:
    """Run-local URL and file caches; no implicit discovery or persistent stale cache."""

    def __init__(self, root, fetch=False):
        self.root = Path(root).resolve()
        self.fetch = fetch
        self.cache, self.files = {}, {}
        self.hits, self.network_requests = 0, 0

    def load(self, item):
        url = checked_url(item["url"])
        if url in self.cache:
            self.hits += 1
            return copy.deepcopy(self.cache[url])
        record = {"url": url, "final_url": url, "status": "unverified", "http_status": None,
                  "kind": "observed", "captured_at": None, "source_ref": None,
                  "sha256": None, "reason": None, "text": ""}
        snap = item.get("snapshot")
        if snap:
            record.update({k: snap[k] for k in ("kind", "captured_at", "http_status", "final_url") if k in snap})
            record["source_ref"] = snap.get("path")
            if snap["status"] != "ok":
                record["reason"] = snap["reason"]
                record["acquisition_status"] = snap["status"]
            else:
                path = (self.root / snap["path"]).resolve()
                require(path.is_relative_to(self.root), "Snapshot path must stay inside the input folder")
                try:
                    if path not in self.files:
                        with path.open("rb") as handle:
                            raw = handle.read(LIMIT + 1)
                        require(len(raw) <= LIMIT, "Snapshot exceeds 3 MiB")
                        self.files[path] = raw
                    self._complete(record, self.files[path])
                except (OSError, UnicodeError) as exc:
                    record["reason"] = f"snapshot_unreadable:{exc.__class__.__name__}"
        elif self.fetch:
            self.network_requests += 1
            record["captured_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
            record["source_ref"] = url
            request = Request(url, headers={"User-Agent": "aimegeo-competitor-gap/1.0 (specified-pages-only)"})
            try:
                with urlopen(request, timeout=10) as response:
                    record["http_status"] = response.status
                    record["final_url"] = response.url
                    expected_length = response.length
                    raw = response.read(LIMIT + 1)
                    if len(raw) > LIMIT:
                        record["reason"] = "fetch_failed:response_too_large"
                    else:
                        if expected_length is not None and len(raw) < expected_length:
                            raise IncompleteRead(raw, expected_length - len(raw))
                        self._complete(record, raw, response.headers.get_content_charset() or "utf-8")
            except HTTPError as exc:
                record["http_status"] = exc.code
                record["reason"] = f"http_error:{exc.code}"
                exc.close()
            except (HTTPException, URLError, TimeoutError, OSError, UnicodeError, LookupError) as exc:
                record["reason"] = f"fetch_failed:{exc.__class__.__name__}"
        else:
            record["reason"] = "not_run: no snapshot; network acquisition was not requested"
        self.cache[url] = record
        return copy.deepcopy(record)

    @staticmethod
    def _complete(record, raw, encoding="utf-8-sig"):
        record["text"] = raw.decode(encoding, errors="strict")
        record["sha256"] = hashlib.sha256(raw).hexdigest()
        record["status"] = "ok"
        record["acquisition_status"] = "ok"


def normalize_octets(value):
    """RFC 9309 path matching: decode only unreserved percent octets."""
    value = "".join(c if ord(c) < 128 else "".join(f"%{b:02X}" for b in c.encode("utf-8")) for c in value)
    def replace(match):
        char = chr(int(match.group()[1:], 16))
        return char if char.isascii() and (char.isalnum() or char in "-._~") else match.group().upper()
    return re.sub(r"%[0-9a-fA-F]{2}", replace, value)


def robots_decision(body, crawler, url):
    groups, agents, rules, rules_started = [], [], [], False
    for raw_line in body.removeprefix("\ufeff").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = [p.strip() for p in line.split(":", 1)]
        if key.casefold() == "user-agent":
            if rules_started:
                groups.append((agents, rules))
                agents, rules, rules_started = [], [], False
            if value:
                agents.append(value.casefold())
        elif key.casefold() in {"allow", "disallow"} and agents:
            rules_started = True
            if value:
                rules.append((key.casefold(), value))
    if agents:
        groups.append((agents, rules))
    candidates = []
    for names, directives in groups:
        lengths = [len(n) for n in names if n != "*" and n in crawler.casefold()]
        specificity = max(lengths) if lengths else (0 if "*" in names else -1)
        if specificity >= 0:
            candidates.append((specificity, names, directives))
    best = max((c[0] for c in candidates), default=-1)
    selected = [c for c in candidates if c[0] == best]
    parsed = urlsplit(url)
    path = normalize_octets((parsed.path or "/") + ("?" + parsed.query if parsed.query else ""))
    matches = []
    for _, _, directives in selected:
        for directive, pattern in directives:
            normalized = normalize_octets(pattern)
            anchored = normalized.endswith("$")
            core = normalized[:-1] if anchored else normalized
            expression = "^" + ".*".join(re.escape(p) for p in core.split("*")) + ("$" if anchored else "")
            if re.search(expression, path):
                # The complete normalized rule determines precedence, including
                # wildcard/end-anchor operators, not just its literal portion.
                # normalize_octets yields ASCII, so its length is its byte length.
                length = len(normalized)
                matches.append((length, directive == "allow", directive, pattern))
    winner = max(matches, default=None)
    return {"state": "allowed" if winner is None or winner[1] else "blocked",
            "groups": [c[1] for c in selected],
            "rule": f"{winner[2]}: {winner[3]}" if winner else None,
            "path": path}


def semantic_heading(text, kind):
    label = text.strip().rstrip(":：").strip()
    pattern = (r"参考资料|参考文献|参考来源|参考|资料来源|信息来源|来源|引用来源|references?|sources?|bibliography"
               if kind == "source" else r"faqs?|frequently\s+asked\s+questions|常见问题|常见问答|问答")
    return bool(re.fullmatch(pattern, label, re.I))


def explicit_question(text):
    return text.rstrip().endswith(("?", "？"))


class PageHTML(HTMLParser):
    QA_CONTAINERS = {"section", "article", "aside", "main", "footer", "header", "nav", "body", "details", "div"}
    # These block starts implicitly end a paragraph even without an explicit </p>.
    P_END_START_TAGS = {
        "address", "article", "aside", "blockquote", "details", "div", "dl", "fieldset",
        "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6",
        "header", "hgroup", "hr", "main", "menu", "nav", "ol", "p", "pre", "search",
        "section", "table", "ul",
    }
    P_SCOPE_BOUNDARIES = {"applet", "button", "caption", "html", "marquee", "object",
                          "table", "td", "template", "th"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.blocks, self.links, self.jsonld = [], [], [], []
        self.block_contexts, self.heading_sections = [], []

    def heading_context(self):
        self.heading_sections = [section for section in self.heading_sections
            if section["container"] is None or any(section["container"] is node for node in self.stack)]
        return {kind: any(section[kind] for section in self.heading_sections) for kind in ("source", "faq")}

    def handle_starttag(self, tag, attrs):
        if tag in self.P_END_START_TAGS:
            # A paragraph inside a template/table/button has its own HTML scope.
            for pos in range(len(self.stack) - 1, -1, -1):
                open_tag = self.stack[pos]["tag"]
                if open_tag == "p":
                    self._close_from(pos)
                    break
                if open_tag in self.P_SCOPE_BOUNDARIES:
                    break
        attrs = {key: value or "" for key, value in attrs}
        is_heading = bool(re.fullmatch(r"h[1-6]", tag))
        parent_hidden = bool(self.stack and self.stack[-1]["hidden"])
        hidden = (parent_hidden or tag in {"head", "script", "style", "noscript", "template"}
                  or "hidden" in attrs or attrs.get("aria-hidden", "").casefold() == "true"
                  or bool(re.search(r"display\s*:\s*none|visibility\s*:\s*hidden", attrs.get("style", ""), re.I)))
        # Hidden navigation/headings cannot end a visible FAQ or source region.
        if is_heading and not hidden:
            self.heading_sections = [section for section in self.heading_sections if section["level"] < int(tag[1])]
        context = self.heading_context()
        marker = attrs.get("id", "") + " " + attrs.get("class", "")
        source = (tag == "cite" or bool(re.search(r"sources?|references?|bibliography|参考|来源", marker, re.I))
                  or bool(self.stack and self.stack[-1]["source"]))
        faq = (bool(re.search(r"\bfaqs?\b|常见问题|常见问答|问答", marker, re.I))
               or any(value.rstrip("/").endswith("schema.org/FAQPage") for value in attrs.get("itemtype", "").split())
               or bool(self.stack and self.stack[-1]["faq"]))
        node = {"tag": tag, "attrs": attrs, "text": [], "hidden": hidden, "source": source,
                "faq": faq, "heading_source": context["source"], "heading_faq": context["faq"]}
        # Keep structural ownership internally; flattened output blocks alone cannot
        # tell an unanswered section heading from an unrelated footer paragraph.
        node["qa_path"] = [parent for parent in self.stack if parent["tag"] in self.QA_CONTAINERS]
        node["details_ancestors"] = [parent for parent in self.stack if parent["tag"] == "details"]
        if tag == "summary":
            node["details_parent"] = next((parent for parent in reversed(self.stack) if parent["tag"] == "details"), None)
        if is_heading:
            containers = {"section", "article", "aside", "main", "footer", "body", "div"}
            node["heading_container"] = next((parent for parent in reversed(self.stack) if parent["tag"] in containers),
                                             self.stack[-1] if self.stack else None)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data):
        visible = not self.stack or not self.stack[-1]["hidden"]
        for node in self.stack:
            # Keep script source for JSON-LD, but never feed hidden text to visible ancestors.
            if visible or node["tag"] == "script":
                node["text"].append(data)

    def close(self):
        super().close()
        if self.stack:
            self._close_from(0)

    def handle_endtag(self, tag):
        positions = [i for i, node in enumerate(self.stack) if node["tag"] == tag]
        if not positions:
            return
        self._close_from(positions[-1])

    def _close_from(self, pos):
        closing, self.stack = self.stack[pos:], self.stack[:pos]
        for node in reversed(closing):
            content = " ".join("".join(node["text"]).split())
            attrs = node["attrs"]
            if node["tag"] == "script" and attrs.get("type", "").split(";", 1)[0].strip().casefold() == "application/ld+json":
                self.jsonld.append("".join(node["text"]))
            if not node["hidden"]:
                if re.fullmatch(r"h[1-6]", node["tag"]):
                    source, faq = semantic_heading(content, "source"), semantic_heading(content, "faq")
                    if source or faq:
                        self.heading_sections.append({"level": int(node["tag"][1]), "source": source,
                            "faq": faq, "container": node["heading_container"]})
                if node["tag"] == "summary" and node.get("details_parent") is not None:
                    node["details_parent"]["summary_text"] = content
                if node["tag"] in {"h1", "h2", "h3", "h4", "p", "summary", "details"} and content:
                    self.blocks.append({"tag": node["tag"], "text": content})
                    context = {"faq": node["faq"] or node["heading_faq"],
                               "qa_path": node["qa_path"],
                               "details_ancestors": node["details_ancestors"]}
                    summary = node.get("summary_text")
                    if (node["tag"] == "details" and summary and content.startswith(summary)
                            and (explicit_question(summary) or context["faq"])):
                        answer = content[len(summary):].strip()
                        if answer:
                            context["details_pair"] = {"question": summary, "answer": answer}
                            context["details_node"] = node
                    self.block_contexts.append(context)
                if node["tag"] == "a" and attrs.get("href"):
                    self.links.append({"href": attrs["href"], "text": content,
                                       "source": node["source"] or node["heading_source"] or "cite" in attrs.get("rel", "").split()})


def schema_context(value, inherited=False):
    # Track the active default vocabulary only; language-only contexts inherit it.
    if isinstance(value, str):
        return value.rstrip("/") in {"https://schema.org", "http://schema.org"}
    if isinstance(value, list):
        active = inherited
        for context in value:
            active = schema_context(context, active)
        return active
    if isinstance(value, dict):
        return schema_context(value["@vocab"]) if "@vocab" in value else inherited
    return False


def typed_nodes(value, inherited=False):
    if isinstance(value, list):
        for item in value:
            yield from typed_nodes(item, inherited)
    elif isinstance(value, dict):
        active = schema_context(value["@context"], inherited) if "@context" in value else inherited
        types = value.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if not isinstance(types, list):
            types = []
        full = [t for t in types if isinstance(t, str) and t.startswith(("https://schema.org/", "http://schema.org/"))] if isinstance(types, list) else []
        if active or full:
            normalized = []
            for name in types if active else full:
                if not isinstance(name, str):
                    continue
                if name.startswith(("https://schema.org/", "http://schema.org/")):
                    normalized.append(name.rsplit("/", 1)[-1])
                elif active and ":" not in name and "/" not in name:
                    normalized.append(name)
            if normalized:
                yield value, normalized
        for key, child in value.items():
            if key != "@context":
                yield from typed_nodes(child, active)


def has_term(body, term):
    escaped = re.escape(term)
    # Latin aliases use word boundaries; Chinese brand terms use literal matching.
    expression = r"(?<![A-Za-z0-9_])" + escaped + r"(?![A-Za-z0-9_])" if term.isascii() else escaped
    return re.search(expression, body, re.I) is not None


def same_question_scope(heading, answer):
    """An answer stays inside the question's live region; inner divs are wrappers."""
    question_path, answer_path = heading["qa_path"], answer["qa_path"]
    if question_path:
        scope = question_path[-1]
        position = next((i for i, node in enumerate(answer_path) if node is scope), None)
        if position is None:
            return False
        descendants = answer_path[position + 1:]
    else:
        descendants = answer_path
    # A new semantic region (footer, section, etc.) is not the question's answer;
    # one or several plain layout divs inside the still-open scope are allowed.
    return all(node["tag"] == "div" for node in descendants)


def extract_page(body, url, site):
    parser = PageHTML()
    parser.feed(body)
    parser.close()
    parsed, errors = [], []
    for index, block in enumerate(parser.jsonld):
        try:
            parsed.append(json.loads(block))
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append({"block": index + 1, "error": exc.__class__.__name__})
    nodes = [pair for block in parsed for pair in typed_nodes(block)]
    types = sorted({name for _, names in nodes for name in names})
    names = [site["name"]] + site.get("aliases", [])
    organizations = []
    for node, node_types in nodes:
        if "Organization" not in node_types:
            continue
        if not isinstance(node.get("name"), str) or not any(node["name"].casefold() == n.casefold() for n in names):
            continue
        organizations.append({k: node[k] for k in ("@id", "name", "url", "description", "sameAs", "logo") if k in node})
    entity_fields = sorted({key for org in organizations for key in ("name", "url", "description", "sameAs") if org.get(key)})
    faq = []
    details_questions = {id(context["details_node"]) for context in parser.block_contexts
                         if "details_pair" in context}
    previous = None
    for block, context in zip(parser.blocks, parser.block_contexts):
        if "details_pair" in context:
            faq.append(context["details_pair"])
        if block["tag"] == "p" and previous:
            heading, heading_context = previous
            if (heading["tag"].startswith("h") and not semantic_heading(heading["text"], "faq")
                    and same_question_scope(heading_context, context)
                    and not any(id(node) in details_questions for node in heading_context["details_ancestors"])
                    and (explicit_question(heading["text"]) or heading_context["faq"])):
                faq.append({"question": heading["text"], "answer": block["text"]})
        previous = block, context
    links = []
    for link in parser.links:
        try:
            resolved = urljoin(url, link["href"])
            parts = urlsplit(resolved)
        except ValueError:
            continue
        if parts.scheme in {"http", "https"} and parts.hostname != urlsplit(url).hostname:
            links.append({"url": resolved, "text": link["text"], "explicit_source": link["source"]})
    paragraphs = [b["text"] for b in parser.blocks if b["tag"] == "p"]
    visible = " ".join(b["text"] for b in parser.blocks)
    metrics = {"faq_visible_pairs": len(faq), "brand_organizations": len(organizations),
               "brand_entity_fields": entity_fields, "brand_entity_field_count": len(entity_fields),
               "explicit_source_links": len({l["url"] for l in links if l["explicit_source"]}),
               "external_link_candidates": len({l["url"] for l in links}),
               "schema_types": types, "jsonld_parsed_blocks": len(parsed), "jsonld_invalid_blocks": len(errors),
               "h1_count": sum(b["tag"] == "h1" for b in parser.blocks),
               "h2_count": sum(b["tag"] == "h2" for b in parser.blocks)}
    return {"metrics": metrics, "faq_evidence": faq, "organizations": organizations, "external_links": links,
            "first_paragraph": paragraphs[0] if paragraphs else None,
            "brand_in_first_paragraph": any(has_term(paragraphs[0], n) for n in names) if paragraphs else None,
            "jsonld_errors": errors, "visible_blocks": parser.blocks,
            "warnings": (["no_visible_text: may require rendered export or indicate a non-content response"] if not visible else [])
                        + (["JSON-LD parsed as JSON; this is not complete Schema.org validation"] if parsed else [])}


SIGNALS = [("content", "faq_visible_pairs"), ("entity", "brand_organizations"),
           ("entity", "brand_entity_fields"),
           ("sources", "explicit_source_links"), ("sources", "external_link_candidates"),
           ("technical", "schema_types"), ("technical", "jsonld_parsed_blocks"),
           ("technical", "jsonld_invalid_blocks"), ("content", "h1_count"), ("content", "h2_count")]


def ai_report(samples, sites):
    records = []
    for sample in samples:
        item = copy.deepcopy(sample)
        completed = sample["status"] in {"observed", "simulated"}
        item["mentions"] = ({site["id"]: any(has_term(sample["answer"], n) for n in [site["name"]] + site.get("aliases", []))
                             for site in sites} if completed else None)
        item["native_citation_count"] = (len(sample["native_citations"]) if sample["status"] == "observed" and sample["native_citations"] is not None else None)
        records.append(item)
    observed = [s for s in records if s["status"] == "observed"]
    counted = [s for s in observed if s["native_citation_count"] is not None]
    return {"status": "observed_samples" if observed else "no_observed_samples", "samples": records,
            "observed_answer_denominator": len(observed), "native_citation_denominator": len(counted),
            "native_citation_total": sum(s["native_citation_count"] for s in counted) if counted else None,
            "note": "Mentions are literal text matches, native citations are imported source entries; no AI ranking is inferred."}


def build_report(data, loader):
    validate(data)
    sites, slots = data["sites"], data["comparison"]["page_slots"]
    results = []
    for site in sites:
        result = {k: site[k] for k in ("id", "name", "role")}
        result["pages"] = []
        robots = loader.load(site["robots"]) if site.get("robots") else None
        robots_is_html = bool(robots and re.search(
            r"(?im)^[\s\ufeff]*<(?:!doctype|/?[a-z][\w:-]*(?:\s|/?>))",
            re.sub(r"<!--.*?-->", "", robots["text"], flags=re.S)))
        for slot in slots:
            item = next((p for p in site.get("pages", []) if p["slot"] == slot), None)
            record = loader.load(item) if item else {"status": "unverified", "reason": "page_not_provided", "url": None, "kind": None}
            page = {"slot": slot, "acquisition": {k: v for k, v in record.items() if k != "text"},
                    "analysis_status": "unverified", "signals": None, "robots": {}}
            if record["status"] == "ok":
                page["signals"] = extract_page(record["text"], record["final_url"], site)
                if page["signals"]["visible_blocks"]:
                    page["analysis_status"] = "observed"
                else:
                    page["acquisition"]["reason"] = "no_visible_content; supply rendered HTML or review the response"
            for bot in CRAWLERS:
                robot = {"state": "unverified", "reason": "robots_not_provided_or_unreadable"}
                if robots_is_html:
                    robot["reason"] = "robots_returned_html"
                if robots and robots["status"] == "ok" and record.get("url") and not robots_is_html:
                    final = record.get("final_url", record["url"])
                    origin = lambda u: (urlsplit(u).scheme, urlsplit(u).netloc)
                    if origin(final) == origin(robots["final_url"]) == origin(robots["url"]):
                        robot = robots_decision(robots["text"], bot, final)
                        robot["kind"] = robots["kind"]
                    else:
                        robot["reason"] = "robots_origin_mismatch"
                page["robots"][bot] = robot
            result["pages"].append(page)
        result["robots_acquisition"] = {k: v for k, v in robots.items() if k != "text"} if robots else None
        results.append(result)
    brand = next(r for r in results if r["role"] == "brand")
    comparisons = []
    for competitor in [r for r in results if r["role"] == "competitor"]:
        for slot in slots:
            left = next(p for p in brand["pages"] if p["slot"] == slot)
            right = next(p for p in competitor["pages"] if p["slot"] == slot)
            comparable = (left["analysis_status"] == right["analysis_status"] == "observed"
                          and left["acquisition"]["kind"] == right["acquisition"]["kind"])
            deltas = {key: right["signals"]["metrics"][key] - left["signals"]["metrics"][key]
                      for key in ("faq_visible_pairs", "brand_organizations", "brand_entity_field_count", "explicit_source_links")} if comparable else None
            comparisons.append({"competitor": competitor["id"], "slot": slot,
                                "status": "comparable" if comparable else "unverified",
                                "kind": left["acquisition"]["kind"] if comparable else None,
                                "competitor_minus_brand": deltas})
    return {"version": "1.0.0", "question": data["comparison"]["question"], "page_slots": slots,
            "sites": results, "comparisons": comparisons,
            "ai_observations": ai_report(data.get("ai_samples", []), sites),
            "cache": {"unique_urls": len(loader.cache), "cache_hits": loader.hits,
                      "unique_snapshot_reads": len(loader.files), "network_requests": loader.network_requests}}


def export_report(report, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "evidence.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (out / "竞品差距矩阵.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        header = ["页面范围", "信号类别", "检查项"]
        for site in report["sites"]:
            header += [f"{site['name']}({site['id']})", f"{site['id']}:证据"]
        writer.writerow(["'" + cell if cell.lstrip().startswith(("=", "+", "-", "@")) else cell for cell in header])
        for slot in report["page_slots"]:
            for dimension, key in SIGNALS + [("technical", "robots:" + bot) for bot in CRAWLERS]:
                row = [slot, dimension, key]
                for site in report["sites"]:
                    page = next(p for p in site["pages"] if p["slot"] == slot)
                    acquired = page["acquisition"]
                    evidence = acquired.get("url") or acquired.get("reason")
                    if key.startswith("robots:"):
                        robot = page["robots"][key.split(":", 1)[1]]
                        value = robot["state"]
                        if robot.get("kind") == "simulated":
                            value = "[模拟] " + value
                        evidence = json.dumps({"page": acquired.get("final_url", acquired.get("url")), "decision": robot,
                                               "capture": site["robots_acquisition"]}, ensure_ascii=False)
                    elif page["analysis_status"] != "observed":
                        value = "未验证"
                        evidence = json.dumps(acquired, ensure_ascii=False)
                    else:
                        value = page["signals"]["metrics"][key]
                        if isinstance(value, list):
                            value = ", ".join(value)
                        if acquired["kind"] == "simulated":
                            value = f"[模拟] {value}"
                        evidence = json.dumps({"url": acquired["final_url"], "sha256": acquired["sha256"],
                                               "captured_at": acquired["captured_at"], "source_ref": acquired["source_ref"]}, ensure_ascii=False)
                    # Avoid executing untrusted website or site-name text as spreadsheet formulas.
                    row.extend([str(value), str(evidence)])
                writer.writerow(["'" + cell if cell.lstrip().startswith(("=", "+", "-", "@")) else cell for cell in row])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Comparison JSON; snapshots resolve relative to it")
    parser.add_argument("--out", required=True, type=Path, help="Write evidence.json and 竞品差距矩阵.csv")
    parser.add_argument("--fetch", action="store_true", help="GET only specified URLs lacking snapshot records")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        report = build_report(data, Loader(args.input.parent, args.fetch))
        export_report(report, args.out)
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Input/output error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "completed", "pages_unverified": sum(p["analysis_status"] != "observed" for s in report["sites"] for p in s["pages"]),
                      "ai_status": report["ai_observations"]["status"], "cache": report["cache"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
