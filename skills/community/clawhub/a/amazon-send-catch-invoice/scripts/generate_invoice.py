#!/usr/bin/env python3
"""Generate one customs invoice .xls from a shipment JSON + your product data.

    python3 generate_invoice.py shipment.json --products products.json
    python3 generate_invoice.py shipment.json --products products.json --template invoice.xls
    python3 generate_invoice.py --check-template invoice.xls     # detect template drift

    pip3 install xlrd xlwt xlutils pillow

Inputs
------
--template   The .xls workbook the forwarder gave you. The script fills it in
             place, preserving formatting, and reads the destination-address
             sheet out of it. Never rebuild this file from scratch — the portal
             validates against its exact structure.

--products   Your product data, as JSON. See reference/product-data-schema.md.
             This is deliberately a plain file: export it from whatever system
             of record you already have (ERP, database, spreadsheet). The agent
             should ASK THE USER where their product data lives rather than
             inventing HS codes or declared values.

shipment.json  One shipment (one FBA id). See reference/shipment-schema.md.

Column layout lives in --layout (default layout.json next to this script) so a
template revision can be absorbed by editing JSON, not code. Run
--check-template after any template update from the forwarder.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import cache_dir, records_dir  # noqa: E402

DEFAULT_LAYOUT = Path(__file__).resolve().parent / "layout.json"


def load_json(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# ── address book ─────────────────────────────────────────────────────────────
def build_address_lookup(template_path, layout) -> dict:
    """Read the destination-address sheet out of the template itself.

    The forwarder maintains this sheet; it maps a warehouse code to the address
    their system expects. Reading it from the template (instead of keeping your
    own copy) means a template update automatically brings new warehouses.
    """
    import xlrd
    cfg = layout["address_sheet"]
    book = xlrd.open_workbook(str(template_path))
    try:
        sheet = book.sheet_by_name(cfg["name"])
    except Exception:                                    # noqa: BLE001
        names = book.sheet_names()
        raise SystemExit(
            f"address sheet {cfg['name']!r} not found. Sheets present: {names}\n"
            "The forwarder probably revised the template — update layout.json "
            "('address_sheet.name') and re-run --check-template.") from None

    lookup = {}
    for r in range(cfg.get("first_row", 1), sheet.nrows):
        code = str(sheet.cell(r, cfg["columns"]["code"]).value).strip()
        if not code:
            continue
        lookup[code] = {k: sheet.cell(r, c).value
                        for k, c in cfg["columns"].items() if k != "code"}
    return lookup


# ── image placement ──────────────────────────────────────────────────────────
def place_square_bitmap(ws, img_path, row, col, px=48):
    """Insert a px-by-px BMP so Excel renders it 1:1.

    xlwt's _position_image() computes the anchor box from the row height and
    column width AT THE MOMENT OF INSERTION. If the image is taller than the
    cell, the anchor spans several rows and Excel stretches the image to fill
    it — the classic "tall and narrow" distortion.

    The trap: Worksheet.row_height() reads Row.__height_in_pixels, and that
    attribute is only updated by set_style(). Assigning row.height does NOT
    touch it (it stays at the default 17px). So "set the row height, then
    insert" does not work; you must write the name-mangled private attribute.

    Column width uses the inverse of xlwt's own formula:
        width_in_pixels = round(width * 0.0272 + 0.446)

    With both at px, the anchor box is exactly one cell and the image is 1:1.

    Verify by reading the file back: rowinfo_map[r].height / 15 and the pixel
    width derived from colinfo_map[col] should both equal px.
    """
    r = ws.row(row)
    r.height_mismatch = 1          # tell Excel to honour an explicit row height
    r.height = px * 15             # twips; 1px ~= 15 twips at 96dpi
    r._Row__height_in_pixels = px  # what xlwt actually reads when anchoring
    ws.col(col).width = int(round((px - 0.446) / 0.0272))
    ws.insert_bitmap(str(img_path), row, col)


# ── template drift check ─────────────────────────────────────────────────────
def check_template(template_path, layout):
    """Compare the template's header row against the layout mapping.

    Run this whenever the forwarder sends a new template. A silently shifted
    column produces an invoice that looks right and is rejected at upload — or,
    worse, is accepted with values in the wrong fields.
    """
    import xlrd
    book = xlrd.open_workbook(str(template_path))
    sheet = book.sheet_by_index(0)
    header_row = layout["data"]["header_row"]
    print(f"template : {template_path}")
    print(f"sheets   : {book.sheet_names()}")
    print(f"header   : row {header_row + 1}\n")

    problems = []
    for field, spec in layout["data"]["columns"].items():
        col = spec["col"]
        actual = str(sheet.cell(header_row, col).value).strip() if col < sheet.ncols else ""
        expected = spec.get("header", "")
        ok = (not expected) or (expected in actual) or (actual in expected and actual)
        print(f"  {'ok ' if ok else 'X  '} col {col:>2}  {field:<18} "
              f"expected~{expected!r}  actual={actual!r}")
        if not ok:
            problems.append(field)

    try:
        book.sheet_by_name(layout["address_sheet"]["name"])
        print(f"\n  ok  address sheet {layout['address_sheet']['name']!r}")
    except Exception:                                    # noqa: BLE001
        problems.append("address_sheet")
        print(f"\n  X   address sheet {layout['address_sheet']['name']!r} MISSING")

    if problems:
        print(f"\n{len(problems)} mismatch(es): {problems}")
        print("The template appears to have changed. Update layout.json, then have "
              "the user upload ONE regenerated invoice as a test before doing a batch.")
        return 1
    print("\nTemplate matches layout.json.")
    return 0


# ── main generation ──────────────────────────────────────────────────────────
def generate(shipment_path, products_path, template_path, layout_path=DEFAULT_LAYOUT,
             out_dir=None) -> Path:
    import xlrd
    from xlutils.copy import copy as xl_copy

    shipment = load_json(shipment_path)
    products = load_json(products_path).get("products", {})
    layout = load_json(layout_path)
    template_path = Path(template_path)
    out_dir = Path(out_dir) if out_dir else records_dir()

    ticket = shipment["ticket"]
    boxes = shipment["boxes"]

    missing = {i["product_key"] for b in boxes for i in b.get("items", [])
               if i["product_key"] not in products}
    if missing:
        print(f"!  not found in product data, fields will be blank: {sorted(missing)}")

    has_battery = any(products.get(i["product_key"], {}).get("has_battery")
                      for b in boxes for i in b.get("items", []))
    has_magnet = any(products.get(i["product_key"], {}).get("has_magnet")
                     for b in boxes for i in b.get("items", []))

    addresses = build_address_lookup(template_path, layout)
    book = xlrd.open_workbook(str(template_path), formatting_info=True)
    wb = xl_copy(book)
    ws = wb.get_sheet(0)

    warehouse = boxes[0].get("warehouse_code", "") if boxes else ""
    fba_id = boxes[0].get("fba_shipment_id", "") if boxes else ""

    # ── order header ─────────────────────────────────────────────────────────
    hdr = layout["header"]
    labels = layout.get("labels", {})

    def put(key, value):
        cell = hdr.get(key)
        if cell and value not in (None, ""):
            ws.write(cell[0], cell[1], value)

    put("waybill_number", fba_id)
    put("customer_reference", fba_id)
    put("total_packages", len(boxes))
    put("destination_country", ticket.get("dest_country", "US"))
    put("channel", ticket.get("channel", ""))
    put("customs_type", ticket.get("customs_type", ""))
    put("has_battery", labels["battery_yes"] if has_battery else labels["battery_no"])
    put("has_magnet", labels["magnet_yes"] if has_magnet else labels["magnet_no"])

    # ── consignee: write the address-book code, then the resolved fields ──────
    put("address_code", warehouse)
    addr = addresses.get(warehouse, {})
    if addr:
        for field, cell in hdr.get("address_fields", {}).items():
            ws.write(cell[0], cell[1], addr.get(field, ""))
    else:
        print(f"!  warehouse {warehouse!r} not in the template's address sheet")

    # ── clear the data area, keeping formatting ──────────────────────────────
    data = layout["data"]
    first = data["first_row"]
    n_rows = sum(len(b.get("items", [])) for b in boxes)
    for r in range(first, first + max(n_rows + 3, 10)):
        for c in range(data["clear_columns"]):
            ws.write(r, c, "")

    # ── one row per box per line item ────────────────────────────────────────
    cols = {k: v["col"] for k, v in data["columns"].items()}
    img_px = layout.get("image", {}).get("px", 48)
    row = first

    for box in boxes:
        seq = box.get("box_seq", 1)
        # Use the box id the inbound API returned, verbatim. Its format is
        # FBA<id>U000001 — U plus SIX digits. Deriving U{seq:05d} yields five
        # digits, which will not match the physical box label.
        box_code = box.get("box_code", "")
        if not box_code:
            print(f"!  box {seq}: no box_code — take it from listShipmentBoxes' boxId")

        for item in box.get("items", []):
            p = products.get(item["product_key"], {})
            qty = item["qty"]                   # quantity IN THIS BOX

            def w(field, value):
                if field in cols and value not in (None, ""):
                    ws.write(row, cols[field], value)

            w("box_seq", seq)
            w("box_code", box_code)
            w("fba_id", box.get("fba_shipment_id", ""))
            w("reference_id", box.get("reference_id", ""))
            w("name_zh", p.get("name_zh", ""))
            w("name_en", p.get("name_en", ""))
            w("hs_code", p.get("hs_code", ""))
            w("unit_price", p.get("declared_unit_price", ""))
            w("qty_per_box", qty)
            # The portal validates qty_total == qty_per_box ON EVERY ROW. It is
            # a per-row check, not a shipment total. Writing the cross-box total
            # here fails every multi-box shipment with a confusing message about
            # "box count x per-box quantity != total quantity".
            w("qty_total", qty)
            w("material", p.get("material", ""))
            w("use", p.get("use", ""))

            if "image" in cols:
                img = cache_dir() / f"{item['product_key']}.bmp"
                if img.exists():
                    try:
                        place_square_bitmap(ws, img, row, cols["image"], img_px)
                    except Exception as e:               # noqa: BLE001
                        print(f"!  image {img.name}: {e}")
                else:
                    print(f"!  no image for {item['product_key']} — run fetch_images.py")

            row += 1

    # ── save ─────────────────────────────────────────────────────────────────
    stamp = date.today().strftime("%Y-%m-%d")
    channel = str(ticket.get("channel", "")).replace("/", "-")
    label = ticket.get("label") or fba_id
    parts = [stamp] + ([channel] if channel else []) + [label, f"{len(boxes)}box"]
    out_path = out_dir / ("_".join(parts) + ".xls")
    wb.save(str(out_path))

    print(f"ok  {out_path}")
    print(f"    {fba_id} -> {warehouse}, {row - first} declaration rows, {len(boxes)} box(es)")
    for box in boxes:
        if not box.get("reference_id"):
            print(f"!   box {box.get('box_seq')}: reference_id is empty")
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shipment", nargs="?")
    ap.add_argument("--products")
    ap.add_argument("--template")
    ap.add_argument("--layout", default=str(DEFAULT_LAYOUT))
    ap.add_argument("--out-dir")
    ap.add_argument("--check-template", metavar="TEMPLATE.xls")
    args = ap.parse_args()

    if args.check_template:
        sys.exit(check_template(args.check_template, load_json(args.layout)))

    if not (args.shipment and args.products and args.template):
        ap.error("need shipment.json, --products and --template "
                 "(or use --check-template)")
    generate(args.shipment, args.products, args.template, args.layout, args.out_dir)


if __name__ == "__main__":
    main()
