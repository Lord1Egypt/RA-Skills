#!/usr/bin/env python3
"""Inspect and export CorelDRAW CDR content through CorelDRAW COM automation.

Requires Windows, installed CorelDRAW, and pywin32.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import win32com.client
except ImportError as exc:  # pragma: no cover - depends on host OS/Python
    raise SystemExit(
        "pywin32 is required. Install with: py -3 -m pip install --user pywin32"
    ) from exc


FORMAT_CONSTANTS = {
    "png": "cdrPNG",
    "jpg": "cdrJPEG",
    "jpeg": "cdrJPEG",
    "pdf": "cdrPDF",
    "svg": "cdrSVG",
    "eps": "cdrEPS",
}


def connect_corel(progid: str | None = None, visible: bool = False):
    candidates = [progid] if progid else [
        "CorelDRAW.Application",
        "CorelDRAW.Application.25",
        "CorelDRAW.Application.24",
        "CorelDRAW.Application.23",
        "CorelDRAW.Application.22",
    ]
    last_error: Exception | None = None
    for candidate in candidates:
        if not candidate:
            continue
        try:
            app = win32com.client.gencache.EnsureDispatch(candidate)
            app.Visible = visible
            return app
        except Exception as exc:  # COM availability is host-dependent
            last_error = exc
    raise RuntimeError(f"Could not start CorelDRAW automation. Last error: {last_error}")


def constants():
    return win32com.client.constants


def const_value(name: str, fallback: int | None = None) -> int:
    try:
        return int(getattr(constants(), name))
    except Exception:
        if fallback is None:
            raise
        return fallback


def get_page(doc, page_number: int):
    if page_number < 1 or page_number > doc.Pages.Count:
        raise ValueError(f"Page {page_number} is outside 1..{doc.Pages.Count}")
    return doc.Pages.Item(page_number)


def get_layer(page, layer_ref: str | None):
    if not layer_ref:
        for idx in range(1, page.Layers.Count + 1):
            layer = page.Layers.Item(idx)
            try:
                if layer.Printable:
                    return layer
            except Exception:
                pass
        return page.Layers.Item(page.Layers.Count)
    if layer_ref.isdigit():
        return page.Layers.Item(int(layer_ref))
    return page.Layers.Item(layer_ref)


def shape_row(page_index: int, layer_index: int, shape_index: int, layer, shape) -> dict:
    name = getattr(shape, "Name", "") or ""
    return {
        "page": page_index,
        "layer_index": layer_index,
        "layer_name": getattr(layer, "Name", ""),
        "shape_index": shape_index,
        "name": name,
        "type": int(getattr(shape, "Type", 0)),
        "x": float(getattr(shape, "PositionX", 0.0)),
        "y": float(getattr(shape, "PositionY", 0.0)),
        "width": float(getattr(shape, "SizeWidth", 0.0)),
        "height": float(getattr(shape, "SizeHeight", 0.0)),
    }


def inspect_document(path: Path, progid: str | None, visible: bool) -> dict:
    app = connect_corel(progid, visible)
    doc = app.OpenDocument(str(path))
    try:
        data = {
            "file": str(path),
            "full_file_name": getattr(doc, "FullFileName", str(path)),
            "pages": [],
        }
        for page_index in range(1, doc.Pages.Count + 1):
            page = doc.Pages.Item(page_index)
            page_data = {
                "index": page_index,
                "name": getattr(page, "Name", ""),
                "width": float(getattr(page, "SizeWidth", 0.0)),
                "height": float(getattr(page, "SizeHeight", 0.0)),
                "layers": [],
            }
            for layer_index in range(1, page.Layers.Count + 1):
                layer = page.Layers.Item(layer_index)
                layer_data = {
                    "index": layer_index,
                    "name": getattr(layer, "Name", ""),
                    "visible": bool(getattr(layer, "Visible", False)),
                    "printable": bool(getattr(layer, "Printable", False)),
                    "shape_count": int(layer.Shapes.Count),
                    "shapes": [],
                }
                for shape_index in range(1, layer.Shapes.Count + 1):
                    shape = layer.Shapes.Item(shape_index)
                    layer_data["shapes"].append(shape_row(page_index, layer_index, shape_index, layer, shape))
                page_data["layers"].append(layer_data)
            data["pages"].append(page_data)
        return data
    finally:
        doc.Close()
        app.Quit()


def parse_index_spec(spec: str) -> list[int]:
    result: list[int] = []
    for part in re.split(r"[,\s]+", spec.strip()):
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            step = 1 if end >= start else -1
            result.extend(range(start, end + step, step))
        else:
            result.append(int(part))
    if not result:
        raise ValueError(f"Empty shape index spec: {spec!r}")
    if any(i < 1 for i in result):
        raise ValueError(f"Shape indexes are one-based: {spec!r}")
    return result


def parse_item(item: str) -> tuple[str, list[int]]:
    if ":" not in item:
        raise ValueError("Item must be filename:indexes, e.g. tree.png:4 or cluster.png:7-20")
    filename, spec = item.split(":", 1)
    filename = filename.strip()
    if not filename:
        raise ValueError(f"Missing filename in --item {item!r}")
    return filename, parse_index_spec(spec)


def create_selection(layer, indexes: list[int]):
    if len(indexes) == 1:
        selection = layer.Shapes.Item(indexes[0])
    else:
        selection = layer.Shapes.Range(indexes)
    selection.CreateSelection()
    return selection


def export_bitmap(doc, out_path: Path, fmt: str, dpi: int, transparent: bool):
    fmt_const = const_value(FORMAT_CONSTANTS[fmt], 802 if fmt == "png" else None)
    selection_range = const_value("cdrSelection", 2)
    rgb_image = const_value("cdrRGBColorImage", 4)
    export_filter = doc.ExportBitmap(
        str(out_path),
        fmt_const,
        selection_range,
        rgb_image,
        0,
        0,
        dpi,
        dpi,
        1,
        False,
        transparent,
        True,
        False,
        0,
        None,
        None,
    )
    export_filter.Finish()


def export_vector(doc, out_path: Path, fmt: str):
    fmt_const = const_value(FORMAT_CONSTANTS[fmt])
    selection_range = const_value("cdrSelection", 2)
    exported = doc.ExportEx(str(out_path), fmt_const, selection_range, None, None)
    try:
        exported.Finish()
    except Exception:
        pass


def export_items(args) -> list[dict]:
    input_path = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    app = connect_corel(args.progid, args.visible)
    doc = app.OpenDocument(str(input_path))
    rows: list[dict] = []
    try:
        page = get_page(doc, args.page)
        layer = get_layer(page, args.layer)
        items: list[tuple[str, list[int]]] = [parse_item(i) for i in args.item]
        if args.all_top_level:
            width = max(2, len(str(layer.Shapes.Count)))
            ext = args.format
            items.extend((f"{args.prefix}_{i:0{width}d}.{ext}", [i]) for i in range(1, layer.Shapes.Count + 1))
        if not items:
            raise ValueError("Provide --item at least once or use --all-top-level")

        for filename, indexes in items:
            out_path = out_dir / filename
            if out_path.exists() and not args.overwrite:
                raise FileExistsError(f"Refusing to overwrite existing file: {out_path}")
            create_selection(layer, indexes)
            fmt = args.format.lower()
            if fmt in {"png", "jpg", "jpeg"}:
                export_bitmap(doc, out_path, fmt, args.dpi, args.transparent)
            else:
                export_vector(doc, out_path, fmt)
            rows.append({
                "filename": out_path.name,
                "path": str(out_path),
                "shape_indexes": " ".join(str(i) for i in indexes),
                "bytes": out_path.stat().st_size,
            })
        if args.manifest:
            with Path(args.manifest).open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=["filename", "path", "shape_indexes", "bytes"])
                writer.writeheader()
                writer.writerows(rows)
        return rows
    finally:
        doc.Close()
        app.Quit()


def export_preview(args):
    input_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    app = connect_corel(args.progid, args.visible)
    doc = app.OpenDocument(str(input_path))
    try:
        get_page(doc, args.page).Activate()
        fmt = out_path.suffix.lower().lstrip(".") or "png"
        if fmt not in {"png", "jpg", "jpeg"}:
            fmt = "png"
        fmt_const = const_value(FORMAT_CONSTANTS[fmt], 802 if fmt == "png" else None)
        current_page = const_value("cdrCurrentPage", 1)
        rgb_image = const_value("cdrRGBColorImage", 4)
        width = args.width or 0
        height = args.height or 0
        export_filter = doc.ExportBitmap(
            str(out_path), fmt_const, current_page, rgb_image,
            width, height, args.dpi, args.dpi, 1,
            False, False, True, False, 0, None, None,
        )
        export_filter.Finish()
        return out_path
    finally:
        doc.Close()
        app.Quit()


def print_inspection(data: dict):
    print(f"Document: {data['full_file_name']}")
    for page in data["pages"]:
        print(f"PAGE {page['index']}: {page['name']} size={page['width']:.3f}x{page['height']:.3f}")
        for layer in page["layers"]:
            print(
                f"  LAYER {layer['index']}: {layer['name']} "
                f"shapes={layer['shape_count']} visible={layer['visible']} printable={layer['printable']}"
            )
            for shape in layer["shapes"]:
                name = shape["name"] or "<unnamed>"
                print(
                    f"    SHAPE {shape['shape_index']}: name={name} type={shape['type']} "
                    f"x={shape['x']:.3f} y={shape['y']:.3f} "
                    f"w={shape['width']:.3f} h={shape['height']:.3f}"
                )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect/export CorelDRAW CDR files through CorelDRAW COM automation.")
    parser.add_argument("--progid", help="CorelDRAW COM ProgID, e.g. CorelDRAW.Application.25")
    parser.add_argument("--visible", action="store_true", help="Show CorelDRAW during automation")
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_p = sub.add_parser("inspect", help="List pages, layers, and top-level shapes")
    inspect_p.add_argument("input")
    inspect_p.add_argument("--json", dest="json_path", help="Write full inspection metadata as JSON")

    preview_p = sub.add_parser("preview", help="Export a full-page preview image")
    preview_p.add_argument("input")
    preview_p.add_argument("output")
    preview_p.add_argument("--page", type=int, default=1)
    preview_p.add_argument("--dpi", type=int, default=300)
    preview_p.add_argument("--width", type=int, default=0)
    preview_p.add_argument("--height", type=int, default=0)

    export_p = sub.add_parser("export", help="Export selected shapes or shape ranges")
    export_p.add_argument("input")
    export_p.add_argument("output")
    export_p.add_argument("--page", type=int, default=1)
    export_p.add_argument("--layer", help="Layer index or name; defaults to first printable layer")
    export_p.add_argument("--item", action="append", default=[], help="filename:indexes, e.g. tree.png:4 or cluster.png:7-20")
    export_p.add_argument("--all-top-level", action="store_true", help="Export every top-level shape in the selected layer")
    export_p.add_argument("--prefix", default="shape", help="Prefix for --all-top-level exports")
    export_p.add_argument("--format", default="png", choices=sorted(FORMAT_CONSTANTS.keys()))
    export_p.add_argument("--dpi", type=int, default=300)
    export_p.add_argument("--transparent", action=argparse.BooleanOptionalAction, default=True)
    export_p.add_argument("--overwrite", action="store_true")
    export_p.add_argument("--manifest", help="Write CSV manifest")

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "inspect":
        data = inspect_document(Path(args.input), args.progid, args.visible)
        print_inspection(data)
        if args.json_path:
            Path(args.json_path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    elif args.command == "preview":
        out = export_preview(args)
        print(out)
    elif args.command == "export":
        rows = export_items(args)
        print(f"Exported {len(rows)} file(s)")
        for row in rows:
            print(f"{row['filename']} <- {row['shape_indexes']} ({row['bytes']} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
