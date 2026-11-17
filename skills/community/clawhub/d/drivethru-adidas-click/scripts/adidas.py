#!/usr/bin/env python3
"""adidas Click B2B toolkit — single CLI entrypoint for all adidas-click tools.

Usage:
    python3 scripts/adidas.py <action> [--username U --password P --base-url URL]
    # non-credential arguments are a JSON object on stdin

adidas Click has no public API, so every action drives the B2B portal with
Playwright. Arguments are a JSON object on stdin whose keys match the tool's
parameters; the result is a single JSON object on stdout (or `{"error": {...}}`
with a non-zero exit code on failure).

Credentials come from (later wins): the `ADIDAS_CLICK_*` environment variables,
the stdin JSON (`username`, `password`, `base_url`), or the CLI flags
`--username` / `--password` / `--base-url`. The flags let you run locally with
no env vars and without putting secrets in the order JSON:

    echo '{"purchase_order": {...}, "confirm": false}' \
        | python3 scripts/adidas.py create-purchase-order --username "$U" --password "$P"

Actions:
    create-purchase-order      Place a B2B purchase order (browser-driven).
                               WRITE — needs "confirm": true to submit; otherwise
                               fills the cart/checkout and returns a dry-run
                               preview. {"purchase_order": {"po_number", "lines":
                               [...], "ship_to": {...}}, "confirm": false}
    check-inventory-pricing    Check live inventory and/or wholesale pricing
                               WITHOUT ordering. READ — inventory reads product
                               pages (no cart); pricing fills a throwaway
                               "DO NOT BUY" cart, reads the priced checkout, then
                               deletes it. {"check": "inventory|pricing|both",
                               "lines": [{"style", "size?", "quantity?"}]}
    get-order-tracking         Get carrier tracking numbers for one or more PO
                               numbers. READ — searches the order book per PO,
                               opens each matching order, and reads its Delivery
                               Tracking table; an order that has not shipped
                               reports its EXPECTED ship dates instead. Nothing
                               is written. {"po_numbers": ["P13434", "P13433"]}
"""

from __future__ import annotations

import os
import sys

# Ensure sibling modules import by bare name regardless of CWD.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import run  # noqa: E402
from adidas_tools import (  # noqa: E402
    adidas_check_inventory_pricing,
    adidas_create_purchase_order,
    adidas_get_order_tracking,
)

ACTIONS = {
    "create-purchase-order": adidas_create_purchase_order,
    "check-inventory-pricing": adidas_check_inventory_pricing,
    "get-order-tracking": adidas_get_order_tracking,
}


if __name__ == "__main__":
    run(
        ACTIONS,
        usage=(
            "adidas.py <"
            + "|".join(ACTIONS)
            + "> [--username U --password P --base-url URL]   # other args: JSON on stdin"
        ),
    )
