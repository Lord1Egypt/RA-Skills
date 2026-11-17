from __future__ import annotations

import html
import json
from html.parser import HTMLParser
from typing import Any, Iterator


class _DocumentMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.scripts: list[tuple[str, str]] = []
        self.meta: list[dict[str, str]] = []
        self._script_type: str | None = None
        self._script_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.casefold(): value or "" for key, value in attrs}
        if tag.casefold() == "script" and self._script_type is None:
            self._script_type = attributes.get("type", "").casefold().split(";", 1)[0].strip()
            self._script_chunks = []
        elif tag.casefold() == "meta":
            self.meta.append(attributes)

    def handle_data(self, data: str) -> None:
        if self._script_type is not None:
            self._script_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "script" and self._script_type is not None:
            self.scripts.append((self._script_type, "".join(self._script_chunks)))
            self._script_type = None
            self._script_chunks = []


def _parse_document(html_text: str) -> _DocumentMetadataParser:
    parser = _DocumentMetadataParser()
    try:
        parser.feed(html_text or "")
        parser.close()
    except Exception:
        pass
    return parser


def parse_json_scripts(html_text: str, mime_type: str) -> list[Any]:
    payloads: list[Any] = []
    wanted_type = mime_type.casefold()
    for script_type, script_text in _parse_document(html_text).scripts:
        if script_type != wanted_type:
            continue
        # Script data is raw text. Entity-unescaping here can turn a valid JSON
        # string such as "A &quot;Quoted&quot; Book" into invalid JSON.
        raw = script_text.strip()
        if raw.startswith("<!--") and raw.endswith("-->"):
            raw = raw[4:-3].strip()
        if not raw:
            continue
        try:
            payloads.append(json.loads(raw))
        except (TypeError, ValueError):
            continue
    return payloads


def iter_json_objects(payload: Any) -> Iterator[dict[str, Any]]:
    if isinstance(payload, list):
        for item in payload:
            yield from iter_json_objects(item)
        return
    if not isinstance(payload, dict):
        return
    yield payload
    graph = payload.get("@graph")
    if isinstance(graph, (dict, list)):
        yield from iter_json_objects(graph)


def has_schema_type(payload: dict[str, Any], expected_type: str) -> bool:
    raw_type = payload.get("@type")
    values = raw_type if isinstance(raw_type, list) else [raw_type]
    expected = expected_type.casefold()
    for value in values:
        normalized = str(value or "").rstrip("/").rsplit("/", 1)[-1].casefold()
        if normalized == expected:
            return True
    return False


def meta_content(html_text: str, *, property_name: str) -> str:
    wanted = property_name.casefold()
    for attributes in _parse_document(html_text).meta:
        key = (attributes.get("property") or attributes.get("name") or "").casefold()
        if key == wanted:
            return html.unescape(attributes.get("content") or "").strip()
    return ""
