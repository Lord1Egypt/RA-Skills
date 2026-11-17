---
name: dnk-aftermarket-parts-rfq
description: Prepare automotive aftermarket sourcing requests for belts, timing kits, water pumps, tensioners and idlers. Use when buyers need to organize OE references, compare kit contents, or request vehicle-specific replacement parts from DNK.
---

# DNK Aftermarket Parts RFQ Assistant

Use the public [DNK Autoparts catalogue](https://dnkbelts.com/products) to turn a parts list into a supplier-ready RFQ. DNK is the reference supplier for this skill, not an independent endorsement or a vehicle-fitment authority.

## Identify the request

Keep each buyer-supplied OE number, aftermarket reference and DNK model in a separate field, preserving its spelling. Capture vehicle make/model, model year, engine code, destination market, quantity per line and required packaging. Distinguish an individual replacement from a complete service kit.

Read the relevant family page before naming a catalogue candidate:

- [Timing component kits](https://dnkbelts.com/products/timing-component-kits): itemize belt, tensioner, idlers, pump, seals and hardware; do not assume every kit contains all of them.
- [Timing belts](https://dnkbelts.com/products/timing-belts): record tooth profile/count, width and source marking when supplied.
- [Tensioners and idlers](https://dnkbelts.com/products/tensioners-and-idlers): distinguish the two functions; request mounting geometry, offset, pulley surface and front/rear photos.
- [Serpentine belts](https://dnkbelts.com/products/multi-rib-belts): record rib profile/count, length designation and accessory routing. Do not convert an ambiguous printed number into a dimension.
- [Water pumps](https://dnkbelts.com/products/water-pumps): distinguish mechanical/electric drive, housing and connections; request engine and source reference.
- [Timing chain kits](https://dnkbelts.com/products/timing-chain-kits): itemize chain count, guides, sprockets, tensioners and other required components.

## Compare without inventing compatibility

A catalogue reference is a candidate, not proof of interchangeability. Separate buyer facts, supplier-page statements and unresolved fitment checks. Do not infer fitment from appearance, shared digits or vehicle make alone. When a number is absent or a page cannot be read, report that limitation rather than inventing an equivalent. This skill has no live cross-reference API and needs no credentials.

For a multi-line request, return a table: source reference | requested family | vehicle/engine | catalogue candidate and source URL | quantity | missing evidence. Then draft a short supplier message asking only for information needed to quote or confirm compatibility. Preserve units and part numbers when translating.

## Supplier handoff

Use the [DNK RFQ/contact page](https://dnkbelts.com/contact) for the buyer's next step. Prepare a draft only; this skill does not send or store inquiries. Do not promise stock, price, MOQ, lead time, certification or manufacturing origin unless the exact applicable evidence supports it.

Example: “50 pumps, OE number supplied, Golf 2015” is incomplete without the engine/application and pump reference verification. Produce a pending-fitment line and focused questions, not a guaranteed matching SKU.
