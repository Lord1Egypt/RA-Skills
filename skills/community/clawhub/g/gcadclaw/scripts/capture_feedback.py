"""Capture pygcadwin entity feedback as JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pygcadwin import Gcad, iter_layout_entities


def _safe_attr(entity: Any, name: str) -> Any:
    try:
        value = getattr(entity, name)
    except Exception:
        return None
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _entity_record(entity: Any) -> dict[str, Any]:
    return {
        "handle": _safe_attr(entity, "Handle"),
        "object_name": _safe_attr(entity, "ObjectName"),
        "layer": _safe_attr(entity, "Layer"),
        "color": _safe_attr(entity, "Color"),
        "linetype": _safe_attr(entity, "Linetype"),
        "lineweight": _safe_attr(entity, "LineWeight"),
        "closed": _safe_attr(entity, "Closed"),
        "text": _safe_attr(entity, "TextString"),
    }


def capture(layout: str | None = None, limit: int | None = None) -> dict[str, Any]:
    cad = Gcad(create_if_missing=True, visible=True)
    try:
        doc = cad.document
        entities = [
            _entity_record(entity)
            for entity in iter_layout_entities(doc, layout=layout, limit=limit)
        ]
        return {
            "document": doc.name,
            "layout": layout or "Model",
            "count": len(entities),
            "entities": entities,
        }
    finally:
        cad.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture pygcadwin entity feedback JSON.")
    parser.add_argument("--out", required=True, help="Output JSON path.")
    parser.add_argument("--layout", help="Layout name. Omit for model space.")
    parser.add_argument("--limit", type=int, help="Maximum entities to enumerate.")
    args = parser.parse_args()

    result = capture(layout=args.layout, limit=args.limit)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Written: {target}")


if __name__ == "__main__":
    main()
