#!/usr/bin/env python3
"""Deterministic pre-fetch executor for OpenClaw agents.

Reads a claim response JSON from stdin (or file argument), executes the
task's execution_recipe without any LLM involvement, and outputs extracted
data as JSON to stdout.

Exit codes:
    0  - Extraction succeeded; stdout contains artifact-ready JSON
    1  - Cannot pre-fetch (no recipe / extraction failed); needs full LLM
    2  - Network error (retryable)
    3  - Partial success; stdout contains extracted data for LLM validation

Zero external dependencies — Python 3 standard library only.
Ported from clawforce/worker/agent.py RecipeExecutor with additions
for html_extract and css_extract recipe types.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser

EXIT_OK = 0
EXIT_NEEDS_LLM = 1
EXIT_NETWORK_ERROR = 2
EXIT_PARTIAL = 3

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _deep_get(obj: dict, dotted_key: str):
    for key in dotted_key.split("."):
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return None
    return obj


def _validate_url(url: str) -> str | None:
    if not url or not url.strip():
        return "empty_url"
    if re.search(r"\{+\w", url):
        return "unresolved_template_variable"
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception as e:
        return f"url_parse_error:{e}"
    if parsed.scheme not in ("http", "https"):
        return f"invalid_scheme:{parsed.scheme or 'missing'}"
    if not parsed.netloc:
        return "missing_host"
    return None


def _http_get(url: str, headers: dict | None = None, timeout: int = 20) -> bytes:
    hdrs = {"User-Agent": USER_AGENT}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# ---------------------------------------------------------------------------
# JSON extraction (ported from RecipeExecutor._extract_json)
# ---------------------------------------------------------------------------

def _extract_json(raw: bytes, flow: dict, scraped_at: str) -> list[dict]:
    try:
        data = json.loads(raw)
    except Exception as e:
        return [{"status": "failed", "error": f"json_parse:{e}", "scraped_at": scraped_at}]

    root = data
    for key in (flow.get("items_root") or "").split("."):
        if key and isinstance(root, dict):
            root = root.get(key, [])

    skip = flow.get("skip_first", 0)
    raw_items = root[skip:] if isinstance(root, list) else []

    field_map = flow.get("field_map", {})
    transforms = flow.get("transforms", {})
    items = []
    for entry in raw_items:
        item: dict = {"status": "ok", "scraped_at": scraped_at}
        for out_key, src_key in field_map.items():
            val = _deep_get(entry, src_key) if "." in src_key else entry.get(src_key)
            if val is None:
                continue
            if transforms.get(out_key) == "ms_to_sec" and isinstance(val, (int, float)):
                item[out_key] = str(round(val / 1000))
            elif isinstance(val, str):
                item[out_key] = val[:500]
            else:
                item[out_key] = val
        items.append(item)
    return items


# ---------------------------------------------------------------------------
# XML extraction (ported from RecipeExecutor._extract_xml)
# ---------------------------------------------------------------------------

def _extract_xml(raw: bytes, flow: dict, scraped_at: str) -> list[dict]:
    try:
        root = ET.fromstring(raw)
    except Exception as e:
        return [{"status": "failed", "error": f"xml_parse:{e}", "scraped_at": scraped_at}]

    ns_map: dict[str, str] = flow.get("namespace", {})
    selector = flow.get("items_selector", "channel/item")
    parts = selector.split("/")

    current = root
    for part in parts[:-1]:
        found = current.find(part)
        if found is not None:
            current = found

    raw_items = current.findall(parts[-1])

    field_map = flow.get("field_map", {})
    items = []
    for entry in raw_items:
        item: dict = {"status": "ok", "scraped_at": scraped_at}
        for out_key, src_key in field_map.items():
            if ":" in src_key:
                prefix, local = src_key.split(":", 1)
                ns_uri = ns_map.get(prefix, "")
                val = entry.findtext(f"{{{ns_uri}}}{local}" if ns_uri else local, "")
            else:
                val = entry.findtext(src_key, "")
            if val:
                item[out_key] = val.strip()[:500]
        items.append(item)
    return items


# ---------------------------------------------------------------------------
# HTML / CSS selector extraction (new — stdlib only)
# ---------------------------------------------------------------------------

class _HtmlExtractor(HTMLParser):
    """Minimal CSS-selector-based HTML extractor using stdlib HTMLParser.

    Supports selectors:
        .classname     — match by class
        #id            — match by id
        tagname        — match by tag
        tag.class      — match by tag + class
        selector@attr  — extract attribute instead of text content
    """

    def __init__(self, item_selector: str, field_selectors: dict[str, str], max_items: int = 200):
        super().__init__()
        self._item_sel = self._parse_selector(item_selector)
        self._field_sels = {k: self._parse_field_selector(v) for k, v in field_selectors.items()}
        self._max_items = max_items

        self._items: list[dict] = []
        self._in_item = False
        self._depth = 0
        self._item_depth = 0
        self._current_item: dict = {}

        self._capture_field: str | None = None
        self._capture_attr: str | None = None
        self._capture_depth = 0
        self._text_buf: list[str] = []

    @staticmethod
    def _parse_selector(sel: str) -> dict:
        result: dict = {}
        if not isinstance(sel, str) or not sel.strip():
            return result
        # Strip attribute selectors like [class*='foo'] or [attr="bar"]
        bracket = sel.find("[")
        if bracket != -1:
            sel = sel[:bracket].strip()
        if not sel:
            return result
        # For descendant/child selectors ("h3 a", "div > span"), use the last token
        parts = sel.strip().split()
        if len(parts) > 1:
            sel = parts[-1].lstrip(">").strip()
        if sel.startswith("#"):
            result["id"] = sel[1:]
        elif sel.startswith("."):
            # ".class-name" — take first class only
            result["class"] = sel[1:].split(".")[0]
        elif "." in sel:
            tag, cls = sel.split(".", 1)
            result["tag"] = tag.lower()
            # Multi-class "p.instock.availability" — take first class after tag
            result["class"] = cls.split(".")[0]
        else:
            result["tag"] = sel.lower()
        return result

    @staticmethod
    def _parse_field_selector(sel) -> dict:
        # Accept dict format: {"selector": "p.price_color", "attribute": "text"}
        if isinstance(sel, dict):
            attr = sel.get("attribute", "")
            sel_str = sel.get("selector", "")
            parsed = _HtmlExtractor._parse_selector(sel_str)
            # "text" means capture inner text (default behaviour — no "attr" key needed)
            if attr and attr != "text":
                parsed["attr"] = attr
            return parsed
        # Accept string format: "p.price_color" or "h3 a@title"
        attr = None
        if "@" in sel:
            sel, attr = sel.rsplit("@", 1)
        parsed = _HtmlExtractor._parse_selector(sel)
        if attr:
            parsed["attr"] = attr
        return parsed

    def _matches(self, tag: str, attrs: list[tuple[str, str | None]], selector: dict) -> bool:
        attr_dict = {k: (v or "") for k, v in attrs}
        if "tag" in selector and tag.lower() != selector["tag"]:
            return False
        if "id" in selector and attr_dict.get("id") != selector["id"]:
            return False
        if "class" in selector:
            classes = attr_dict.get("class", "").split()
            if selector["class"] not in classes:
                return False
        return True

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        self._depth += 1

        if not self._in_item:
            if self._matches(tag, attrs, self._item_sel) and len(self._items) < self._max_items:
                self._in_item = True
                self._item_depth = self._depth
                self._current_item = {}
            return

        if self._capture_field is None:
            for field_name, sel in self._field_sels.items():
                if field_name in self._current_item:
                    continue
                if self._matches(tag, attrs, sel):
                    if "attr" in sel:
                        attr_dict = {k: (v or "") for k, v in attrs}
                        val = attr_dict.get(sel["attr"], "")
                        if val:
                            self._current_item[field_name] = val[:500]
                    else:
                        self._capture_field = field_name
                        self._capture_depth = self._depth
                        self._text_buf = []
                    break

    def handle_endtag(self, tag: str):
        if self._capture_field is not None and self._depth == self._capture_depth:
            text = " ".join(self._text_buf).strip()
            if text:
                self._current_item[self._capture_field] = text[:500]
            self._capture_field = None
            self._text_buf = []

        if self._in_item and self._depth == self._item_depth:
            if self._current_item:
                self._items.append(self._current_item)
            self._in_item = False
            self._current_item = {}

        self._depth -= 1

    def handle_data(self, data: str):
        if self._capture_field is not None:
            stripped = data.strip()
            if stripped:
                self._text_buf.append(stripped)

    @property
    def items(self) -> list[dict]:
        return self._items


def _extract_html(raw: bytes, extraction: dict, scraped_at: str) -> list[dict]:
    item_selector = extraction.get("item_selector", "")
    fields = extraction.get("fields", {})
    max_items = extraction.get("max_items", 200)

    if not item_selector or not fields:
        return []

    try:
        html_text = raw.decode("utf-8", errors="replace")
    except Exception:
        return []

    parser = _HtmlExtractor(item_selector, fields, max_items)
    try:
        parser.feed(html_text)
    except Exception:
        return []

    items = []
    for entry in parser.items:
        entry["status"] = "ok"
        entry["scraped_at"] = scraped_at
        items.append(entry)
    return items


# ---------------------------------------------------------------------------
# Recipe execution dispatcher
# ---------------------------------------------------------------------------

def _resolve_url(spec: dict) -> str:
    for key in ("target_url", "url", "podcast_url", "feed_url", "site_url", "_url_template_override"):
        v = spec.get(key)
        if isinstance(v, str) and v:
            return v
    return ""


def _build_params(spec: dict) -> dict:
    url = _resolve_url(spec)
    params = {"target_url": url, "podcast_url": url}
    for k, v in spec.items():
        if isinstance(v, (str, int, float)):
            params[k] = v
    params["max_episodes"] = min(int(spec.get("max_episodes", 50)), 200)
    return params


def execute_l1_http(flow: dict, params: dict) -> tuple[list[dict], str | None]:
    scraped_at = _now()
    try:
        url = flow["url_template"].format(**params)
    except KeyError as e:
        return [], f"missing_param:{e}"

    err = _validate_url(url)
    if err:
        return [], err

    try:
        raw = _http_get(url)
    except Exception as e:
        return [], f"network:{e}"

    resp_type = flow.get("response_type", "json")
    if resp_type == "json":
        items = _extract_json(raw, flow, scraped_at)
    elif resp_type == "xml":
        items = _extract_xml(raw, flow, scraped_at)
    else:
        return [], f"unsupported_response_type:{resp_type}"

    ok_count = sum(1 for i in items if i.get("status") == "ok")
    if ok_count == 0:
        return items, "zero_ok_items"
    return items, None


def execute_routed(recipe: dict, params: dict) -> tuple[list[dict], str | None]:
    url = params.get("target_url") or params.get("podcast_url", "")
    err = _validate_url(url)
    if err:
        return [], err

    for route in recipe.get("routes", []):
        m = re.search(route["pattern"], url)
        if m:
            if route.get("url_param") and m.lastindex:
                params[route["url_param"]] = m.group(1)
            sub_flow = recipe.get("sub_flows", {}).get(route["sub_flow"])
            if not sub_flow:
                return [], f"missing_sub_flow:{route['sub_flow']}"
            return execute_l1_http(sub_flow, params)

    return [], "no_matching_route"


def execute_html_extract(recipe: dict, spec: dict) -> tuple[list[dict], str | None]:
    scraped_at = _now()
    fetch_config = recipe.get("fetch", {})
    extraction = recipe.get("extraction", {})

    if not extraction.get("item_selector") or not extraction.get("fields"):
        return [], "missing_extraction_config"

    url_template = fetch_config.get("url_template", "{target_url}")
    params = _build_params(spec)
    try:
        url = url_template.format(**params)
    except KeyError as e:
        return [], f"missing_param:{e}"

    err = _validate_url(url)
    if err:
        return [], err

    headers = fetch_config.get("headers")
    try:
        raw = _http_get(url, headers=headers)
    except Exception as e:
        return [], f"network:{e}"

    items = _extract_html(raw, extraction, scraped_at)

    if not items:
        fallback = recipe.get("fallback")
        if fallback == "llm_extract":
            return [], "html_extract_empty_fallback_llm"
        return [], "html_extract_empty"

    return items, None


def execute_css_extract(recipe: dict, spec: dict) -> tuple[list[dict], str | None]:
    """Lab Auto css_extract compatibility — same logic as html_extract."""
    adapted = {
        "type": "html_extract",
        "fetch": {"url_template": "{target_url}"},
        "extraction": {
            "item_selector": recipe.get("item_selector", ""),
            "fields": recipe.get("fields", {}),
            "max_items": 200,
        },
        "fallback": recipe.get("fallback", "llm_extract"),
    }
    pagination = recipe.get("pagination")
    if pagination and pagination.get("next"):
        pass  # pagination not supported in prefetch — single page only
    return execute_html_extract(adapted, spec)


def execute_recipe(recipe: dict, spec: dict) -> tuple[list[dict], str | None]:
    """Dispatch to the appropriate executor based on recipe type.

    Returns (items, error_reason).
    error_reason is None on success, a string describing why it failed otherwise.
    """
    recipe_type = recipe.get("type", "")
    params = _build_params(spec)

    if recipe_type in ("l1_http",):
        return execute_l1_http(recipe, params)
    if recipe_type == "routed":
        return execute_routed(recipe, params)
    if recipe_type == "html_extract":
        return execute_html_extract(recipe, spec)
    if recipe_type == "css_extract":
        return execute_css_extract(recipe, spec)
    return [], f"unsupported_recipe_type:{recipe_type}"


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1]) as f:
            claim_data = json.load(f)
    else:
        claim_data = json.load(sys.stdin)

    spec = claim_data.get("structured_spec") or {}
    agent_ctx = claim_data.get("agent_context") or {}
    recipe = (
        claim_data.get("execution_recipe")
        or spec.get("execution_recipe")
        or agent_ctx.get("execution_recipe")
        or {}
    )
    prefetch_hint = agent_ctx.get("prefetch_hint") or {}

    if prefetch_hint.get("can_prefetch") is False:
        sys.exit(EXIT_NEEDS_LLM)

    if not recipe and prefetch_hint.get("extraction"):
        recipe = {
            "type": "html_extract",
            "fetch": {"url_template": "{target_url}"},
            "extraction": prefetch_hint["extraction"],
            "fallback": "llm_extract",
        }

    if not recipe or not recipe.get("type"):
        sys.exit(EXIT_NEEDS_LLM)

    try:
        items, error = execute_recipe(recipe, spec)
    except Exception as e:
        print(f"[PREFETCH] Unexpected error: {e}", file=sys.stderr)
        if "network" in str(e).lower() or "urlopen" in str(e).lower():
            sys.exit(EXIT_NETWORK_ERROR)
        sys.exit(EXIT_NEEDS_LLM)

    if error:
        print(f"[PREFETCH] {error}", file=sys.stderr)
        if error.startswith("network:"):
            sys.exit(EXIT_NETWORK_ERROR)
        sys.exit(EXIT_NEEDS_LLM)

    ok_items = [i for i in items if i.get("status") == "ok"]
    if not ok_items:
        print("[PREFETCH] No successful items extracted", file=sys.stderr)
        sys.exit(EXIT_NEEDS_LLM)

    task_type = claim_data.get("task_type", "custom")
    has_fallback = recipe.get("fallback") == "llm_extract"

    avg_fields = sum(
        len([v for k, v in it.items() if k not in ("status", "scraped_at")])
        for it in ok_items
    ) / len(ok_items) if ok_items else 0
    expected_fields = len(recipe.get("extraction", {}).get("fields", {}))

    needs_validation = (
        has_fallback
        and expected_fields > 0
        and avg_fields < expected_fields * 0.5
    )

    output = {
        "items": ok_items,
        "item_count": len(ok_items),
        "executor": "prefetch_partial" if needs_validation else "prefetch",
        "recipe_type": recipe.get("type", ""),
        "scraped_at": _now(),
        "task_type": task_type,
        "confidence": "unverified" if needs_validation else "high",
    }

    json.dump(output, sys.stdout, ensure_ascii=False)
    sys.exit(EXIT_PARTIAL if needs_validation else EXIT_OK)


if __name__ == "__main__":
    main()
