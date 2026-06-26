---
name: filament-vault
description: "Track 3D printing filament inventory locally. Add spools, log usage, check stock levels, and generate spending reports. Use when: filament, spool, 3d print inventory, filament stock, what filament do I have, printing materials, filament vault, filament inventory, low stock filament."
---

# filament-vault

Local filament inventory tracker. All data stored in JSON at `~/.openclaw/workspace/filament-vault/inventory.json`.

## Scripts

All scripts live in `scripts/`. Run with `python3 scripts/<script>.py [args]`.

## Add a Spool

```
python3 scripts/add_spool.py --brand "Bambu" --material PLA --color "Matte Black" --weight 1000 --cost 19.99 --location "Shelf A"
```

Options: `--brand`, `--material` (PLA/PETG/ABS/TPU/Nylon/ASA/other), `--color`, `--weight` (grams, default 1000), `--cost` (USD), `--location`, `--notes`

## Update / Use a Spool

```
python3 scripts/update_spool.py --search "matte black" --used 150
python3 scripts/update_spool.py --id <uuid> --finished --notes "Ran out mid-print"
```

Options: `--id` (UUID), `--search` (partial match), `--used` (grams consumed), `--finished` (mark empty), `--notes`

## List Inventory

```
python3 scripts/inventory.py
python3 scripts/inventory.py --material PLA --low-stock
python3 scripts/inventory.py --json
```

Filters: `--material`, `--color`, `--brand`, `--low-stock` (under threshold, default 100g), `--threshold <g>`, `--json`

## Generate Report

```
python3 scripts/report.py
python3 scripts/report.py --threshold 200
```

Shows: total spools, total weight, total value, by-material breakdown, low-stock alerts, monthly spending.

## Search

```
python3 scripts/search.py "bambu"
python3 scripts/search.py "black petg" --json
```

Fuzzy search across all fields (brand, color, material, location, notes).

## References

See `references/materials.md` for filament material properties and guidance.
