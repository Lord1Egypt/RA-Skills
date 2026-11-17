#!/usr/bin/env python3
"""Inspect, edit, and export CorelDRAW CDR files through CorelDRAW COM automation.

Requires Windows, installed CorelDRAW, and pywin32.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Iterable, Any

try:
    import win32com.client
except ImportError as exc:  # pragma: no cover
    raise SystemExit("pywin32 is required. Install with: py -3 -m pip install --user pywin32") from exc

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
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Could not start CorelDRAW automation. Last error: {last_error}")


def const_value(name: str, fallback: int | None = None) -> int:
    try:
        return int(getattr(win32com.client.constants, name))
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
    if str(layer_ref).isdigit():
        return page.Layers.Item(int(layer_ref))
    return page.Layers.Item(layer_ref)


def parse_index_spec(spec: str) -> list[int]:
    result: list[int] = []
    for part in re.split(r"[,\s]+", str(spec).strip()):
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            step = 1 if end >= start else -1
            result.extend(range(start, end + step, step))
        else:
            result.append(int(part))
    if not result or any(i < 1 for i in result):
        raise ValueError(f"Invalid one-based shape index spec: {spec!r}")
    return result


def create_selection(layer, indexes: list[int]):
    selection = layer.Shapes.Item(indexes[0]) if len(indexes) == 1 else layer.Shapes.Range(indexes)
    selection.CreateSelection()
    return selection


def shape_rows(doc) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for page_i in range(1, doc.Pages.Count + 1):
        page = doc.Pages.Item(page_i)
        for layer_i in range(1, page.Layers.Count + 1):
            layer = page.Layers.Item(layer_i)
            for shape_i in range(1, layer.Shapes.Count + 1):
                shape = layer.Shapes.Item(shape_i)
                rows.append({
                    "page": page_i,
                    "page_name": getattr(page, "Name", ""),
                    "layer": layer_i,
                    "layer_name": getattr(layer, "Name", ""),
                    "shape": shape_i,
                    "name": getattr(shape, "Name", "") or "",
                    "type": int(getattr(shape, "Type", 0)),
                    "x": float(getattr(shape, "PositionX", 0.0)),
                    "y": float(getattr(shape, "PositionY", 0.0)),
                    "width": float(getattr(shape, "SizeWidth", 0.0)),
                    "height": float(getattr(shape, "SizeHeight", 0.0)),
                })
    return rows


def inspect(args) -> None:
    app = connect_corel(args.progid, args.visible)
    doc = app.OpenDocument(str(Path(args.input)))
    try:
        rows = shape_rows(doc)
        print(f"Document: {getattr(doc, 'FullFileName', args.input)}")
        for page_i in range(1, doc.Pages.Count + 1):
            page = doc.Pages.Item(page_i)
            print(f"PAGE {page_i}: {getattr(page, 'Name', '')} size={page.SizeWidth:.3f}x{page.SizeHeight:.3f}")
            for layer_i in range(1, page.Layers.Count + 1):
                layer = page.Layers.Item(layer_i)
                print(f"  LAYER {layer_i}: {getattr(layer, 'Name', '')} shapes={layer.Shapes.Count} visible={layer.Visible} printable={layer.Printable}")
                for row in [r for r in rows if r['page'] == page_i and r['layer'] == layer_i]:
                    name = row['name'] or '<unnamed>'
                    print(f"    SHAPE {row['shape']}: name={name} type={row['type']} x={row['x']:.3f} y={row['y']:.3f} w={row['width']:.3f} h={row['height']:.3f}")
        if args.json:
            Path(args.json).write_text(json.dumps(rows, indent=2), encoding="utf-8")
    finally:
        doc.Close()
        app.Quit()


def export_bitmap(doc, out_path: Path, fmt: str, dpi: int, transparent: bool):
    export_filter = doc.ExportBitmap(
        str(out_path),
        const_value(FORMAT_CONSTANTS[fmt], 802 if fmt == "png" else None),
        const_value("cdrSelection", 2),
        const_value("cdrRGBColorImage", 4),
        0, 0, dpi, dpi, 1,
        False, transparent, True, False, 0, None, None,
    )
    export_filter.Finish()


def export_vector(doc, out_path: Path, fmt: str):
    exported = doc.ExportEx(str(out_path), const_value(FORMAT_CONSTANTS[fmt]), const_value("cdrSelection", 2), None, None)
    try:
        exported.Finish()
    except Exception:
        pass


def parse_item(item: str) -> tuple[str, list[int]]:
    if ":" not in item:
        raise ValueError("Use filename:indexes, e.g. logo.png:4 or cluster.png:7-20")
    filename, spec = item.split(":", 1)
    return filename.strip(), parse_index_spec(spec)


def export(args) -> None:
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    app = connect_corel(args.progid, args.visible)
    doc = app.OpenDocument(str(Path(args.input)))
    rows = []
    try:
        layer = get_layer(get_page(doc, args.page), args.layer)
        items = [parse_item(item) for item in args.item]
        if args.all_top_level:
            width = max(2, len(str(layer.Shapes.Count)))
            items.extend((f"{args.prefix}_{i:0{width}d}.{args.format}", [i]) for i in range(1, layer.Shapes.Count + 1))
        if not items:
            raise ValueError("Provide --item or --all-top-level")
        for filename, indexes in items:
            out_path = out_dir / filename
            if out_path.exists() and not args.overwrite:
                raise FileExistsError(f"Refusing to overwrite existing file: {out_path}")
            create_selection(layer, indexes)
            if args.format in {"png", "jpg", "jpeg"}:
                export_bitmap(doc, out_path, args.format, args.dpi, args.transparent)
            else:
                export_vector(doc, out_path, args.format)
            rows.append({"filename": out_path.name, "path": str(out_path), "shape_indexes": " ".join(map(str, indexes)), "bytes": out_path.stat().st_size})
        if args.manifest:
            with Path(args.manifest).open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=["filename", "path", "shape_indexes", "bytes"])
                writer.writeheader()
                writer.writerows(rows)
        for row in rows:
            print(f"{row['filename']} <- {row['shape_indexes']} ({row['bytes']} bytes)")
    finally:
        doc.Close()
        app.Quit()


def preview(args) -> None:
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    app = connect_corel(args.progid, args.visible)
    doc = app.OpenDocument(str(Path(args.input)))
    try:
        get_page(doc, args.page).Activate()
        fmt = out_path.suffix.lower().lstrip(".") or "png"
        if fmt not in {"png", "jpg", "jpeg"}:
            fmt = "png"
        export_filter = doc.ExportBitmap(
            str(out_path), const_value(FORMAT_CONSTANTS[fmt], 802 if fmt == "png" else None), const_value("cdrCurrentPage", 1), const_value("cdrRGBColorImage", 4),
            args.width or 0, args.height or 0, args.dpi, args.dpi, 1,
            False, False, True, False, 0, None, None,
        )
        export_filter.Finish()
        print(out_path)
    finally:
        doc.Close()
        app.Quit()


def load_ops(args) -> list[dict[str, Any]]:
    ops: list[dict[str, Any]] = []
    if args.plan:
        data = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        ops.extend(data if isinstance(data, list) else data.get("operations", []))
    for op_text in args.op or []:
        ops.append(json.loads(op_text))
    if not ops:
        raise ValueError("Provide --op JSON or --plan JSON")
    return ops


def layer_for_op(doc, op: dict[str, Any]):
    return get_layer(get_page(doc, int(op.get("page", 1))), op.get("layer"))


def selection_for_op(doc, op: dict[str, Any]):
    layer = layer_for_op(doc, op)
    return create_selection(layer, parse_index_spec(op["shapes"]))


def apply_one(doc, op: dict[str, Any]) -> None:
    kind = op["op"]
    if kind == "save-copy":
        return
    if kind in {"layer-visible", "layer-printable"}:
        layer = layer_for_op(doc, op)
        value = bool(op.get("value", True))
        if kind == "layer-visible":
            layer.Visible = value
        else:
            layer.Printable = value
        return
    selection = selection_for_op(doc, op)
    if kind == "rename":
        if len(parse_index_spec(op["shapes"])) != 1:
            raise ValueError("rename expects one shape")
        selection.Name = op["name"]
    elif kind == "move":
        selection.Move(float(op.get("dx", 0)), float(op.get("dy", 0)))
    elif kind == "set-position":
        selection.SetPosition(float(op["x"]), float(op["y"]))
    elif kind == "resize":
        selection.SetSize(float(op["width"]), float(op["height"]))
    elif kind == "rotate":
        selection.Rotate(float(op["angle"]))
    elif kind == "duplicate":
        selection.Duplicate(float(op.get("dx", 0)), float(op.get("dy", 0)))
    elif kind == "delete":
        selection.Delete()
    elif kind == "group":
        selection.Group()
    elif kind == "ungroup":
        selection.Ungroup()
    else:
        raise ValueError(f"Unsupported op: {kind}")


def apply_plan(args) -> None:
    input_path = Path(args.input)
    output_path = Path(args.output)
    if input_path.resolve() == output_path.resolve() and not args.in_place:
        raise ValueError("Refusing to edit source in place without --in-place")
    if output_path.exists() and not args.overwrite and not args.in_place:
        raise FileExistsError(f"Refusing to overwrite existing file: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    app = connect_corel(args.progid, args.visible)
    doc = app.OpenDocument(str(input_path))
    try:
        for op in load_ops(args):
            apply_one(doc, op)
        if args.in_place:
            doc.Save()
        else:
            doc.SaveAs(str(output_path), None)
        print(output_path)
    finally:
        doc.Close()
        app.Quit()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect, edit, and export CorelDRAW CDR files through CorelDRAW COM automation.")
    parser.add_argument("--progid", help="CorelDRAW COM ProgID, e.g. CorelDRAW.Application.25")
    parser.add_argument("--visible", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("inspect")
    p.add_argument("input")
    p.add_argument("--json")

    p = sub.add_parser("preview")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--width", type=int, default=0)
    p.add_argument("--height", type=int, default=0)

    p = sub.add_parser("export")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--layer")
    p.add_argument("--item", action="append", default=[])
    p.add_argument("--all-top-level", action="store_true")
    p.add_argument("--prefix", default="shape")
    p.add_argument("--format", default="png", choices=sorted(FORMAT_CONSTANTS))
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--transparent", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--manifest")

    p = sub.add_parser("apply-plan")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--op", action="append", help="Operation JSON object; may be repeated")
    p.add_argument("--plan", help="JSON array or object with operations[]")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--in-place", action="store_true", help="Allow input and output to be the same path")

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "inspect":
        inspect(args)
    elif args.command == "preview":
        preview(args)
    elif args.command == "export":
        export(args)
    elif args.command == "apply-plan":
        apply_plan(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
