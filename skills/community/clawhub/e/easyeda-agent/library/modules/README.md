# Reusable Lib Modules

`catalog.json` is the public, sanitized registry. Records begin as evidence-backed candidates and
advance only when their topology, EasyEDA identities and measured geometry are independently proven.

Run `python3 ../../scripts/modules-audit.py`. See
[`../../references/reusable-module-library.md`](../../references/reusable-module-library.md) for the
data boundary and contribution workflow.

`ams1117-3v3.layout-input.json` is the first executable asset. It contains independently verified
part identities and official-API symbol measurements; run it through `sch lib-layout`, then pass the
generated JSON to `sch compose`. Its PCB and hardware maturity remain explicitly unverified.

The eleven `*.topology.json` files are independent role-based modules extracted directly from a completed
live schematic. They are deliberately split so the public library does not retain an original whole-board
mapping. Project identity, original designators and anonymous source-net names were removed; 32-character
Device UUIDs, every physical pin and connected/unconnected state were kept. They are `topology_ready`, not
`compose_ready`, because the editor timed out when all pin coordinates were requested with geometry in one call.

This directory intentionally contains no copied training PDFs, BOM rows, board names, scoring text,
absolute board coordinates or per-board mappings.
