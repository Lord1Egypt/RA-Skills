#!/usr/bin/env python3
"""Download FBA box labels, split Amazon label from carrier label, square them up.

    python3 get_labels.py <planId>                  # 4x6 thermal, as returned
    python3 get_labels.py <planId> --square         # 100x100mm square stickers
    python3 get_labels.py <planId> --square 80      # 80x80mm
    python3 get_labels.py <planId> --page-type PackageLabel_Letter_2
    python3 get_labels.py <planId> --outdir labels --carrier-prefix catch

Output is flat, one file per label per shipment:

    labels/fba_<FBA id>_<FC>.pdf          Amazon box label
    labels/carrier_<FBA id>_<FC>.pdf      partnered-carrier label

Requires PyMuPDF and numpy:  pip3 install pymupdf numpy
(only for --square and the split; the raw download is stdlib-only)

Where the labels come from
--------------------------
The 2024-03-20 API has NO box-label endpoint. `createMarketplaceItemLabels`
there is for FNSKU item labels, something else entirely. Box labels come from
the v0 API, whose READ operations still work even though its write operations
are deprecated. Asking 2024-03-20 for labels returns 403, which looks like a
permission problem but simply means the path does not exist.

The query parameter is `PackageLabelsToPrint` (repeatable, one per box id).
Amazon's own docs and error messages sometimes call it `cartonIdList` — that is
an internal name and is not accepted.

Box ids come from listShipmentBoxes and only exist after setPackingInformation.

PageType controls page size AND whether the carrier label is included at all
---------------------------------------------------------------------------
    PageType                                  size        pages
    PackageLabel_Letter_2                     8.5x11"     2   FBA page sideways
    PackageLabel_A4_2                         8.3x11.7"   2   FBA page sideways
    PackageLabel_Thermal                      4.2x6.0"    2   carrier page sideways
    PackageLabel_Thermal_No_Carrier_Rotation  4.2x6.0"    2   both upright  <- default
    PackageLabel_Letter_6 / A4_4 /
      Plain_Paper / Thermal_NonPCP            varies      1   NO carrier label
    PackageLabel_Letter_4                     rejected in some marketplaces

The *_NonPCP and single-page types silently drop the partnered-carrier label.
Never use them while shipping with a partnered carrier — you will print a box
label with no carrier label and the shipment will be refused at pickup.
"""
from __future__ import annotations

import argparse
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spapi import ENDPOINT, MARKETPLACE, request  # noqa: E402

BASE = ENDPOINT + "/inbound/fba/2024-03-20"
DEFAULT_PAGETYPE = "PackageLabel_Thermal_No_Carrier_Rotation"
MM = 72 / 25.4          # PDF points per millimetre


def _get(path, params=None):
    return request("GET", BASE + path, params=params)


def split_and_fix(pdf_bytes: bytes, fba_out: Path, carrier_out: Path):
    """Split Amazon's combined PDF into box label and carrier label.

    Classification is by CONTENT, not page index: the Amazon box label carries
    extractable text (addresses, box id), the carrier label is a raster image
    with none. Page order is not guaranteed across PageTypes and multi-box
    shipments, so indexing by page number misfiles labels.

    Also stands up any page whose text runs bottom-to-top. Some PageTypes return
    a page with no /Rotate set but a text direction of (0,-1) — visually
    sideways, structurally "upright". A no-op for the default PageType; a safety
    net for the Letter/A4 ones.
    """
    import fitz                                        # PyMuPDF
    src = fitz.open(stream=pdf_bytes, filetype="pdf")
    fba_pages, carrier_pages = [], []
    for i, page in enumerate(src):
        directions = {tuple(round(v, 2) for v in line["dir"])
                      for block in page.get_text("dict")["blocks"]
                      for line in block.get("lines", [])}
        if (0.0, -1.0) in directions:
            page.set_rotation((page.rotation + 90) % 360)
        (fba_pages if directions else carrier_pages).append(i)

    for pages, out in ((fba_pages, fba_out), (carrier_pages, carrier_out)):
        if not pages:
            continue
        doc = fitz.open()
        doc.insert_pdf(src, from_page=min(pages), to_page=max(pages))
        out.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(out))
        doc.close()
    src.close()
    return len(fba_pages), len(carrier_pages)


def ink_bbox(page, dpi=150):
    """True ink bounds of a page, found by rendering.

    Rendering (rather than reading the text bbox) is what makes barcodes and
    raster-only carrier labels measurable. Returns None for a blank page.
    """
    import fitz
    import numpy as np
    pm = page.get_pixmap(dpi=dpi)
    arr = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width, pm.n)
    ink = (arr[:, :, :3] < 200).any(axis=2)            # any non-white channel
    ys, xs = np.where(ink)
    if not len(xs):
        return None
    scale = 72 / dpi
    return fitz.Rect(xs.min() * scale, ys.min() * scale,
                     (xs.max() + 1) * scale, (ys.max() + 1) * scale)


def to_square(pdf: Path, size_mm=100.0, margin_mm=4.0):
    """Re-lay every page onto a 1:1 square canvas.

    100x100mm is the sticker format most Asian freight forwarders expect. The
    content is clipped to its ink bounds and re-placed centred at a UNIFORM
    scale, so barcodes are never stretched (a stretched barcode may still scan,
    but out-of-spec bar widths get rejected by strict scanners). Content is
    embedded as a vector Form XObject — nothing is rasterised.
    """
    import fitz
    src = fitz.open(str(pdf))
    out = fitz.open()
    side = size_mm * MM
    avail = side - 2 * margin_mm * MM
    for i, page in enumerate(src):
        bb = ink_bbox(page)
        if bb is None:
            continue
        k = min(avail / bb.width, avail / bb.height)     # uniform scale
        w, h = bb.width * k, bb.height * k
        dest = fitz.Rect((side - w) / 2, (side - h) / 2, (side + w) / 2, (side + h) / 2)
        out.new_page(width=side, height=side).show_pdf_page(dest, src, i, clip=bb)
    if out.page_count:
        tmp = pdf.with_suffix(".tmp.pdf")
        out.save(str(tmp))
        tmp.replace(pdf)
    out.close()
    src.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan_id")
    ap.add_argument("--square", nargs="?", const=100.0, type=float, metavar="MM",
                    help="re-lay onto a square canvas, default 100mm")
    ap.add_argument("--page-type", default=DEFAULT_PAGETYPE)
    ap.add_argument("--outdir", default="labels")
    ap.add_argument("--carrier-prefix", default="carrier",
                    help="filename prefix for the forwarder label")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    plan = _get(f"/inboundPlans/{args.plan_id}")
    fmt = f"{args.square:g}x{args.square:g}mm square" if args.square else "as-returned"
    print(f"plan {args.plan_id}  ({plan.get('status')})")
    print(f"PageType={args.page_type}   output={fmt}\n")

    n_fba = n_carrier = 0
    for s in plan.get("shipments", []):
        sid = s["shipmentId"]
        d = _get(f"/inboundPlans/{args.plan_id}/shipments/{sid}")
        fba = d.get("shipmentConfirmationId")
        fc = d.get("destination", {}).get("warehouseId")

        boxes = _get(f"/inboundPlans/{args.plan_id}/shipments/{sid}/boxes").get("boxes", [])
        box_ids = [b["boxId"] for b in boxes if b.get("boxId")]
        if not box_ids:
            print(f"  {fba} {fc}: no boxIds — was setPackingInformation run?")
            continue

        query = [("MarketplaceId", MARKETPLACE), ("PageType", args.page_type),
                 ("LabelType", "UNIQUE")] + [("PackageLabelsToPrint", b) for b in box_ids]
        url = (f"{ENDPOINT}/fba/inbound/v0/shipments/{fba}/labels?"
               + urllib.parse.urlencode(query))
        download_url = request("GET", url)["payload"]["DownloadURL"]
        pdf = urllib.request.urlopen(download_url, timeout=60).read()

        fba_out = outdir / f"fba_{fba}_{fc}.pdf"
        carrier_out = outdir / f"{args.carrier_prefix}_{fba}_{fc}.pdf"
        got_fba, got_carrier = split_and_fix(pdf, fba_out, carrier_out)
        if args.square:
            for got, out in ((got_fba, fba_out), (got_carrier, carrier_out)):
                if got:
                    to_square(out, args.square)
        n_fba += bool(got_fba)
        n_carrier += bool(got_carrier)
        warn = "  ⚠ no carrier label — wrong PageType?" if not got_carrier else ""
        print(f"  {fba} {str(fc):5} {len(box_ids)} box -> "
              f"{fba_out.name}, {carrier_out.name}{warn}")

    print(f"\n{n_fba} FBA + {n_carrier} carrier labels in {outdir}")


if __name__ == "__main__":
    main()
