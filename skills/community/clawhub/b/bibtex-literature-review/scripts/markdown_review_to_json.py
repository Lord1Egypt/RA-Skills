#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CITE_PATTERN = re.compile(
    r"\[(?:cite:([@\w,;\-\s]+)|(@[A-Za-z0-9_:\-.;@\s]+)|(\d+(?:\s*[-,;]\s*\d+)*))\]"
)


def load_references(path: Path) -> list[dict[str, Any]]:
    refs = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(refs, list):
        raise ValueError("References JSON must be a list.")
    normalized = []
    for idx, ref in enumerate(refs, start=1):
        if not isinstance(ref, dict):
            raise ValueError(f"Reference {idx} must be an object.")
        gbt = ref.get("gbt") or ref.get("formatted") or ref.get("text")
        if not gbt:
            raise ValueError(f"Reference {idx} is missing 'gbt', 'formatted', or 'text'.")
        item = dict(ref)
        item["gbt"] = gbt
        item.setdefault("key", f"ref{idx:03d}")
        normalized.append(item)
    return normalized


def split_markdown_paragraphs(text: str) -> list[str]:
    paragraphs = []
    buffer = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if buffer:
                paragraphs.append(" ".join(buffer).strip())
                buffer = []
            continue
        if stripped.startswith("#"):
            continue
        buffer.append(stripped)
    if buffer:
        paragraphs.append(" ".join(buffer).strip())
    return paragraphs


def key_index_map(refs: list[dict[str, Any]]) -> dict[str, int]:
    mapping = {}
    for idx, ref in enumerate(refs, start=1):
        for key_name in ("key", "id", "citation-key", "anchor"):
            value = ref.get(key_name)
            if value:
                mapping[str(value).lstrip("@")] = idx
    return mapping


def parse_cite_token(raw: str, mapping: dict[str, int]) -> list[int]:
    raw = raw.strip()
    if not raw:
        raise ValueError("Empty citation marker.")
    pieces = [piece.strip() for piece in re.split(r"[;,]", raw) if piece.strip()]
    indices: list[int] = []
    for piece in pieces:
        piece = piece.lstrip("@").strip()
        range_match = re.match(r"^(\d+)\s*-\s*(\d+)$", piece)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            step = 1 if end >= start else -1
            indices.extend(range(start, end + step, step))
            continue
        if piece.isdigit():
            indices.append(int(piece))
            continue
        if piece not in mapping:
            raise ValueError(f"Unknown citation key: {piece}")
        indices.append(mapping[piece])
    return indices


def paragraph_to_parts(paragraph: str, mapping: dict[str, int]) -> list[Any]:
    parts: list[Any] = []
    pos = 0
    for match in CITE_PATTERN.finditer(paragraph):
        if match.start() > pos:
            parts.append(paragraph[pos : match.start()])
        raw_cite = next(group for group in match.groups() if group)
        indices = parse_cite_token(raw_cite, mapping)
        if len(indices) == 1:
            parts.append({"cite": indices[0]})
        else:
            collapse = all(indices[i] + 1 == indices[i + 1] for i in range(len(indices) - 1))
            parts.append({"cite": indices, "collapse": collapse})
        pos = match.end()
    if pos < len(paragraph):
        parts.append(paragraph[pos:])
    return parts


def cited_indices(paragraphs: list[list[Any]]) -> list[int]:
    order: list[int] = []
    seen: set[int] = set()
    for paragraph in paragraphs:
        for part in paragraph:
            if not isinstance(part, dict) or "cite" not in part:
                continue
            cite = part["cite"]
            values = [cite] if isinstance(cite, int) else cite
            if not isinstance(values, list):
                raise ValueError(f"Invalid citation value: {cite!r}")
            for idx in values:
                if not isinstance(idx, int):
                    raise ValueError(f"Citation value must be an integer: {idx!r}")
                if idx not in seen:
                    seen.add(idx)
                    order.append(idx)
    return order


def remap_paragraphs(paragraphs: list[list[Any]], index_map: dict[int, int]) -> list[list[Any]]:
    remapped: list[list[Any]] = []
    for paragraph in paragraphs:
        new_parts: list[Any] = []
        for part in paragraph:
            if not isinstance(part, dict) or "cite" not in part:
                new_parts.append(part)
                continue
            cite = part["cite"]
            new_part = dict(part)
            if isinstance(cite, int):
                new_part["cite"] = index_map[cite]
            elif isinstance(cite, list):
                new_part["cite"] = sorted(dict.fromkeys(index_map[idx] for idx in cite))
            else:
                raise ValueError(f"Invalid citation value: {cite!r}")
            new_parts.append(new_part)
        remapped.append(new_parts)
    return remapped


def select_used_references(
    refs: list[dict[str, Any]],
    paragraphs: list[list[Any]],
    keep_unused: bool,
) -> tuple[list[dict[str, Any]], list[list[Any]]]:
    if keep_unused:
        return refs, paragraphs

    order = cited_indices(paragraphs)
    if not order:
        raise ValueError("No citation markers found; refusing to create an uncited bibliography.")
    for idx in order:
        if idx < 1 or idx > len(refs):
            raise ValueError(f"Citation index {idx} is outside references list.")

    index_map = {old_idx: new_idx for new_idx, old_idx in enumerate(order, start=1)}
    selected_refs = [refs[old_idx - 1] for old_idx in order]
    return selected_refs, remap_paragraphs(paragraphs, index_map)


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a Markdown review draft to review JSON.")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--refs", type=Path, required=True, help="Candidate/selected references JSON.")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--title", default="文献综述")
    parser.add_argument(
        "--keep-unused",
        action="store_true",
        help="Keep all input references instead of filtering to references cited in the Markdown draft.",
    )
    args = parser.parse_args()

    refs = load_references(args.refs)
    mapping = key_index_map(refs)
    paragraphs = [
        paragraph_to_parts(paragraph, mapping)
        for paragraph in split_markdown_paragraphs(args.markdown.read_text(encoding="utf-8"))
    ]
    refs, paragraphs = select_used_references(refs, paragraphs, args.keep_unused)
    review = {
        "title": args.title,
        "references": [{"anchor": ref.get("anchor"), "gbt": ref["gbt"]} for ref in refs],
        "paragraphs": paragraphs,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote={args.out}")
    print(f"references={len(refs)}")
    print(f"paragraphs={len(paragraphs)}")
    print(f"unused_references={'kept' if args.keep_unused else 'filtered'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
