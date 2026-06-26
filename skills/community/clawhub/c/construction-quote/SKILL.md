---
name: construction-quote
description: Generate itemised construction quotes, material lists, and job costings from plain English job descriptions. Covers extensions, kitchens, bathrooms, loft conversions, roofing, and general building work with UK material prices and labour rates. Use when a builder, tradesperson, or contractor needs to quote a job or estimate costs.
user-invocable: true
argument-hint: "[job description] or describe the construction/building work"
---

# Construction Quote & Job Costing Calculator

You generate professional, itemised construction quotes from plain English job descriptions. Your output should be something a builder or contractor can use as a working estimate within minutes -- not a vague ballpark, but a structured costing with materials, labour, additional costs, markup, and a client-ready quote document.

**Disclaimer (include at the end of every quote):**
> This is an estimated quote based on typical UK construction costs (2025/26). Actual costs depend on site conditions, access, specifications, material availability, and regional pricing. London prices are typically 20-40% higher; South East 10-20% higher. Always conduct a site visit before issuing a final quote to a client. Get supplier quotes for accurate material costs. This does not constitute a fixed-price contract.

---

## How It Works

The user describes a construction job. You produce a complete itemised quote they can use as a working estimate or adapt into a client quote.

### Information Gathering

If the user provides minimal detail, ask for these essentials (max 4 questions):
1. **What's the job?** (type of work, scope)
2. **Dimensions/size?** (room size, extension footprint, roof area, length of fencing, etc.)
3. **Spec level?** (budget, mid-range, or premium finishes)
4. **Location?** (region affects pricing -- London, South East, Midlands, North, etc.)

If the user provides enough context, skip questions and generate immediately. Use reasonable assumptions and state them clearly.

---

## Job Types

Generate the correct quote structure based on what the user describes. If the job spans multiple trades, combine them into a single quote.

### 1. Kitchen Fitting / Refurbishment
**Typical scope:** Strip out, plastering, electrics (additional sockets, lighting), plumbing (sink relocation, dishwasher/washing machine feeds), tiling (splashbacks/full walls), flooring, unit fitting, worktop templating and fitting, appliance connection
**Key materials:** Kitchen units, worktops (laminate/solid wood/quartz/granite), tiles, adhesive and grout, plasterboard, plaster, electrical cable and accessories, copper/plastic pipe, waste fittings, silicone, flooring
**Trades involved:** Kitchen fitter, electrician, plumber, plasterer, tiler

### 2. Bathroom Fitting / Refurbishment
**Typical scope:** Strip out, plumbing first fix, electrical first fix (fan, lighting, heated towel rail), waterproofing/tanking, wall and floor tiling, sanitaryware installation, second fix plumbing and electrics, silicone and finishing
**Key materials:** Sanitaryware (bath/shower/toilet/basin), tiles, tanking kit, adhesive and grout, plasterboard (moisture-resistant), pipe and fittings, waste, electrical cable, extractor fan, heated towel rail, silicone
**Trades involved:** Plumber, electrician, tiler, plasterer

### 3. Single-Storey Extension
**Typical scope:** Foundations (strip or trench fill), blockwork/brickwork walls, DPC, cavity insulation, lintels, roof structure (flat or pitched), roofing, windows and doors, first fix (electrics, plumbing, carpentry), plastering, second fix, decoration
**Key materials:** Concrete (C25), reinforcement mesh/rebar, DPM, breeze blocks (440x215x100), facing bricks, wall ties, cavity insulation, lintels (concrete/steel), roof timbers or steels, roof covering (tiles/felt/EPDM), fascia and soffit, windows (uPVC/aluminium), bifold or patio doors, plasterboard, plaster, electrical and plumbing materials, flooring
**Trades involved:** Groundworker, bricklayer, roofer, carpenter, electrician, plumber, plasterer, decorator
**Additional:** Building regulations approval required. Planning permission likely required. Party wall considerations if near boundary.

### 4. Double-Storey Extension
**As single-storey plus:** Additional blockwork/brickwork for first floor, floor joists or beam-and-block, staircase (if internal), additional windows, more electrical and plumbing runs
**Note:** Structural engineer design typically required. Significantly higher foundation and structural costs.

### 5. Loft Conversion
**Types:** Velux/rooflight (cheapest -- no structural changes to roof), dormer (flat roof or pitched dormer added), hip-to-gable (hip end converted to vertical gable wall), mansard (both roof slopes altered)
**Typical scope:** Structural steelwork, floor strengthening, stud walls, insulation (between and under rafters), plasterboard and skim, Velux or dormer windows, staircase, electrics, plumbing (if en-suite), fire door to new room, fire doors to existing rooms on escape route, smoke detection
**Key materials:** Steel beams (RSJs), timber joists and noggins, insulation (Celotex/Kingspan or mineral wool), plasterboard, plaster, Velux windows or dormer kit, staircase, fire doors, electrical cable and accessories, plumbing materials (if en-suite)
**Trades involved:** Structural engineer (design), steelworker, carpenter, roofer, electrician, plumber, plasterer, decorator
**Additional:** Building regulations required. Planning permission required for dormers in many areas (especially conservation areas). Party wall if semi-detached/terraced.

### 6. Garage Conversion
**Typical scope:** New front wall (brickwork or stud with insulation), floor insulation and screed (or insulated timber floor), insulated plasterboard to walls and ceiling, electrics, plumbing (if adding WC or utility), window/door in new front wall, plastering, decoration
**Key materials:** Bricks or insulated stud frame, insulation (floor, walls, ceiling), DPM, plasterboard, plaster, electrical and plumbing materials, window, door, flooring
**Trades involved:** Bricklayer, carpenter, electrician, plumber, plasterer, decorator
**Additional:** Building regulations required. Planning permission usually not required (permitted development) but check local conditions.

### 7. Roofing (New, Repair, Flat to Pitched)
**Types:** Full re-roof (strip and re-tile/slate), roof repair (patch, replace broken tiles, re-ridge, re-point verges, repair flashing), flat roof replacement (felt, EPDM, GRP/fibreglass), flat to pitched conversion
**Key materials:** Roof tiles (concrete/clay) or slates (natural/artificial), battens, breathable membrane (e.g. Tyvek), ridge tiles, hip tiles, lead flashing, mortar/dry fix systems, fascia and soffit boards, EPDM/GRP for flat roofs, OSB decking for flat roofs, insulation
**Trades involved:** Roofer, scaffolder, carpenter (if structural work)
**Additional:** Scaffolding almost always required. Flat to pitched needs planning permission and building regulations.

### 8. Plastering and Rendering
**Types:** Skim coat over plasterboard, re-plaster (hack off and re-plaster), external render (sand/cement, monocouche, silicone, lime)
**Key materials:** Multi-finish plaster, bonding plaster, PVA, plasterboard (standard/moisture-resistant/fire-rated), render (sand, cement, lime, or pre-mixed monocouche/silicone), mesh, beads, scrim tape
**Trades involved:** Plasterer, labourer
**Measurement:** Price per m2. Typical rates: skim over plasterboard GBP 8-15/m2 (labour); 2-coat plaster GBP 15-25/m2 (labour); external render GBP 35-60/m2 (labour and materials)

### 9. Electrical Rewire
**Typical scope:** Full rewire (new consumer unit, new circuits, new cable throughout, sockets, switches, light fittings), or partial rewire/upgrade
**Key materials:** Consumer unit (18th Edition compliant), twin and earth cable (various sizes), conduit/trunking, sockets, switches, downlights, junction boxes, back boxes, cable clips, fire-rated downlight covers
**Trades involved:** Electrician (Part P registered), plasterer (for making good)
**Additional:** Electrical Installation Certificate (EIC) required. Building Control notification under Part P. Typically 5-7 days for a 3-bed house.

### 10. Plumbing (New Bathroom, Central Heating)
**Types:** New bathroom plumbing, central heating installation (boiler + radiators), boiler replacement only, underfloor heating
**Key materials:** Boiler (combi/system/regular), radiators, TRVs, copper/plastic pipe and fittings, cylinder (if system boiler), controls (thermostat, programmer), valves, flux, solder or push-fit fittings, sanitaryware
**Trades involved:** Plumber, gas engineer (Gas Safe registered for boiler/gas work)
**Additional:** Gas Safe registration mandatory for any gas work. Building Control notification for boiler replacement.

### 11. Painting and Decorating (Interior/Exterior)
**Types:** Full interior redecoration, single room, exterior painting, wallpapering
**Key materials:** Paint (emulsion for walls/ceilings, satinwood/gloss for woodwork), primer/undercoat, filler, sandpaper, masking tape, dust sheets, wallpaper and paste (if wallpapering), exterior masonry paint, wood stain/preserver
**Trades involved:** Painter/decorator
**Measurement:** Price per room (interior) or per m2 (exterior). Typical rates: single room GBP 300-600 (walls + ceiling + woodwork); exterior front of terraced house GBP 500-1,200

### 12. Fencing and Landscaping
**Types:** Close-board fencing, panel fencing, post and rail, decking, paving, turfing, planting, retaining walls
**Key materials:** Fence panels or featherboard, fence posts (concrete/timber), gravel boards, postcrete/concrete, screws/nails, decking boards and joists, paving slabs or block paving, sand, cement, weed membrane, topsoil, turf
**Trades involved:** Fencer/landscaper, labourer, groundworker (for retaining walls)
**Measurement:** Fencing per linear metre. Decking and paving per m2. Turfing per m2.

### 13. Driveway and Paving
**Types:** Block paving, tarmac, resin-bound, gravel, concrete, natural stone
**Key materials:** Block pavers or chosen surface, sub-base (Type 1 MOT), sharp sand, kiln-dried sand (for block paving), edging, weed membrane, drainage channel
**Trades involved:** Groundworker, block paver/paving specialist
**Additional:** Planning permission required if impermeable surface over 5m2 drains onto the highway (front gardens). Consider permeable paving or soakaway.

### 14. Window and Door Replacement
**Types:** uPVC windows, aluminium windows, timber windows, composite doors, bifold doors, patio/sliding doors
**Key materials:** Window/door units (supply), fixings, expanding foam, silicone, plaster/filler for making good internally, external cill if needed
**Trades involved:** Window fitter, plasterer (making good)
**Additional:** Must comply with Part L (thermal performance). FENSA registration or Building Control sign-off. Typical U-value requirement: 1.4 W/m2K or lower.

### 15. Structural Alterations (RSJs, Knock-Throughs)
**Typical scope:** Structural engineer calculations and drawings, temporary support (Acrow props, needles), removal of wall section, installation of steel beam (RSJ/UB), padstones, bearing onto existing structure, making good
**Key materials:** Steel beam (size per engineer's specification), padstones, Acrow props, strongboy attachments, timber needles, mortar, plaster, plasterboard
**Trades involved:** Structural engineer (design), builder/bricklayer, steelworker
**Additional:** Building regulations approval required. Party Wall Act if shared wall. Structural engineer's certificate needed.

### 16. Damp Proofing and Tanking
**Types:** Rising damp treatment (chemical DPC injection), penetrating damp repair, basement tanking (cementitious or membrane system), condensation solutions
**Key materials:** DPC injection cream (e.g. Dryzone, Wykamol), render (salt-resistant), tanking slurry or membrane, dehumidifier, ventilation units, re-plastering materials
**Trades involved:** Damp proofing specialist, plasterer
**Additional:** Correct diagnosis is critical -- rising damp is frequently misdiagnosed. Many damp issues are caused by condensation or penetrating damp, not rising damp.

---

## Quote Components

For every job, generate all four sections below.

### 1. Material List

Present as a table with low and high estimates:

```
| Material | Quantity | Unit | Unit Price (est.) | Total (est.) |
|---|---|---|---|---|
| Concrete (C25) | 3 | m3 | GBP 85-110 | GBP 255-330 |
| Breeze blocks 440x215x100 | 200 | blocks | GBP 1.20-1.60 | GBP 240-320 |
| Facing bricks | 500 | bricks | GBP 0.50-1.20 | GBP 250-600 |
| ... | | | | |
```

- List every material category relevant to the job
- Use quantity estimates based on the dimensions/scope provided
- Show unit price ranges (low and high) reflecting UK 2025 merchant prices
- State assumptions clearly (e.g. "assumes standard 100mm blockwork walls")

### 2. Labour Breakdown

Present as a table:

```
| Trade | Days | Day Rate (est.) | Total (est.) |
|---|---|---|---|
| Bricklayer | 5 | GBP 180-250 | GBP 900-1,250 |
| Labourer | 5 | GBP 100-160 | GBP 500-800 |
| Electrician | 2 | GBP 200-300 | GBP 400-600 |
| Plumber | 3 | GBP 200-280 | GBP 600-840 |
```

Use these UK trade day rates (2025/26 approximate):

| Trade | Day Rate Range |
|---|---|
| General labourer | GBP 100-160 |
| Bricklayer | GBP 180-250 |
| Carpenter / joiner | GBP 180-250 |
| Electrician | GBP 200-300 |
| Plumber | GBP 200-280 |
| Plasterer | GBP 180-250 |
| Roofer | GBP 200-280 |
| Tiler | GBP 180-250 |
| Painter / decorator | GBP 150-220 |
| Gas engineer | GBP 200-300 |
| Groundworker | GBP 150-220 |
| Kitchen fitter | GBP 180-250 |
| Window fitter | GBP 180-250 |
| Damp specialist | GBP 200-280 |
| Fencer / landscaper | GBP 150-220 |

Lower end = outside London, less experienced. Higher end = London/SE, experienced, or specialist.

### 3. Additional Costs

Include all applicable items:

| Item | Estimated Cost | Notes |
|---|---|---|
| Skip hire (8-yard) | GBP 200-350 | Per skip. Permit extra if on public highway (GBP 20-65). |
| Scaffolding | GBP 500-1,500 | Depends on scope and duration. Weekly hire after initial period. |
| Building Control fees | GBP 200-900 | Based on job value. Full plans or building notice route. |
| Planning application | GBP 206 | Householder application (2025 fee). |
| Party Wall surveyor | GBP 700-1,000 | Per adjoining owner. Required if within 3m/6m of neighbour's foundations or on boundary. |
| Structural engineer | GBP 300-800 | Calculations and drawings. Required for steelwork, underpinning, load-bearing alterations. |
| Tool hire | GBP 50-200 | Specialist tools (e.g. diamond drill, plate compactor, SDS drill) |
| Delivery charges | GBP 30-100 | Per delivery. Bulk materials (aggregates, bricks) often have minimum order values. |
| Asbestos survey / removal | GBP 150-500+ | Required in pre-2000 buildings if disturbing materials. Licensed removal for certain types. |

Only include items relevant to the specific job. Do not pad with irrelevant costs.

### 4. Markup & Summary

Present the final summary:

```
| | Low Estimate | High Estimate |
|---|---|---|
| Materials | GBP X,XXX | GBP X,XXX |
| Labour | GBP X,XXX | GBP X,XXX |
| Waste / skip hire | GBP XXX | GBP XXX |
| Other costs | GBP XXX | GBP XXX |
| **Subtotal** | **GBP X,XXX** | **GBP X,XXX** |
| Waste allowance (10%) | GBP XXX | GBP XXX |
| Profit margin (20%) | GBP X,XXX | GBP X,XXX |
| **Quote Total (ex. VAT)** | **GBP XX,XXX** | **GBP XX,XXX** |
| VAT @ 20% (if VAT registered) | GBP X,XXX | GBP X,XXX |
| **Total inc. VAT** | **GBP XX,XXX** | **GBP XX,XXX** |
```

**Notes on markup:**
- **Waste allowance (10%):** Applied to materials subtotal. Covers off-cuts, breakage, over-ordering, returns.
- **Profit margin (20%):** Applied to full subtotal (materials + labour + waste + other costs). This is the contractor's margin. Adjust if the user specifies a different margin.
- **VAT:** Only include if the contractor is VAT registered (threshold GBP 90,000 from 1 April 2024). Some domestic work may qualify for reduced rate (5%) -- e.g. renovating an empty dwelling. Note this where relevant.

---

## Client-Ready Quote Document

After the detailed breakdown, generate a separate client-ready quote document. This is what the builder sends to the homeowner -- it does NOT show internal margins, trade day rates, or material markup.

### Format:

```
---

[YOUR COMPANY NAME]
[Address Line 1]
[Address Line 2]
[Phone] | [Email]
[Company Registration / VAT Number if applicable]

---

QUOTATION

Quote Ref: [QR-YYYY-XXXX]
Date: [DD/MM/YYYY]
Valid for: 30 days

Client: [Client Name]
Property: [Site Address]

---

JOB DESCRIPTION

[Clear description of the work to be carried out]

---

ITEMISED COSTS

| Item | Cost |
|---|---|
| [Phase/area 1 description] | GBP X,XXX |
| [Phase/area 2 description] | GBP X,XXX |
| [Phase/area 3 description] | GBP X,XXX |
| Waste removal | GBP XXX |
| **Total (ex. VAT)** | **GBP XX,XXX** |
| VAT @ 20% | GBP X,XXX |
| **Total (inc. VAT)** | **GBP XX,XXX** |

---

PAYMENT SCHEDULE

| Stage | Percentage | Amount |
|---|---|---|
| Deposit (on acceptance) | 25% | GBP X,XXX |
| First fix completion | 25% | GBP X,XXX |
| Second fix completion | 25% | GBP X,XXX |
| Practical completion | 25% | GBP X,XXX |

---

ESTIMATED TIMELINE

[Start date: TBC on acceptance]
[Estimated duration: X weeks]
[Key milestones if relevant]

---

WHAT'S INCLUDED

- [List of all work included]
- All materials and labour
- Waste removal
- Building Control application (if applicable)

WHAT'S NOT INCLUDED

- Planning application fees (if required)
- Party Wall surveyor fees (if required)
- Unforeseen structural issues or remedial work
- Decorating/finishing unless specified above
- Client-supplied items (kitchen units, sanitaryware, etc. unless stated)
- Furniture removal or storage
- Asbestos survey or removal (if discovered)

---

TERMS AND CONDITIONS

1. This quote is valid for 30 days from the date above.
2. A written acceptance and deposit payment are required to secure a start date.
3. Any variations to the agreed scope of work will be priced separately and agreed in writing before proceeding.
4. The contractor holds public liability insurance of GBP [X] million.
5. All work will comply with current Building Regulations where applicable.
6. Payment terms: as per the payment schedule above. Final payment due within 7 days of practical completion.
7. Any snagging items identified at practical completion will be rectified within 14 days.
8. Guarantee: [12 months / as per manufacturer's warranty on materials].

Signed: _______________________ Date: ___________
[Company Name]

Accepted: ______________________ Date: ___________
[Client Name]

---
```

**Client quote notes:**
- Group costs by phase or area, not by trade. The client does not need to see individual trade day rates.
- Use a single price per line item (use the midpoint of your range, or the high estimate if quoting conservatively).
- The payment schedule percentages can be adjusted. For smaller jobs (under GBP 5,000), use 50% deposit / 50% completion. For very large jobs (over GBP 50,000), consider monthly valuations.

---

## CIS (Construction Industry Scheme) Notes

Include CIS guidance when the quote involves subcontracting:

- **What is CIS?** HMRC scheme requiring contractors to deduct tax from payments to subcontractors. Applies to construction operations.
- **Deduction rates:**
  - **20%** -- Registered subcontractor (verified with HMRC)
  - **30%** -- Unregistered subcontractor
  - **0%** -- Gross payment status (qualifying contractors with good compliance record)
- **Contractor responsibilities:** Verify subcontractors with HMRC before first payment. Submit monthly CIS returns to HMRC by the 19th of each month. Issue payment and deduction statements to subcontractors.
- **What counts as construction operations:** Building, alterations, repairs, decorating, demolition, installation of heating/lighting/power/water/drainage. Does NOT include architecture, surveying, carpet fitting, or delivering materials.
- **Labour-only subcontractors:** If using self-employed labour, ensure the relationship genuinely qualifies as self-employment (not disguised employment). HMRC's CEST tool can help assess status.

Only include CIS notes when relevant (i.e. when the user is a contractor who will be subcontracting work). Do not include for a homeowner getting a quote.

---

## Regional Pricing Adjustments

Apply these rough regional multipliers to the base estimates:

| Region | Adjustment |
|---|---|
| London (Zones 1-3) | +30-40% |
| London (Zones 4-6) | +20-30% |
| South East (Surrey, Kent, Sussex, Berks, Herts) | +10-20% |
| South West, East Anglia, Midlands | Base rate |
| North West, Yorkshire, North East | -5 to -10% |
| Wales | -5 to -15% |
| Scotland (Central Belt) | Base rate |
| Scotland (Highlands/Islands) | +10-20% (transport costs) |
| Northern Ireland | -5 to -10% |

State the assumed region in the quote. If the user does not specify, use base rate and note it.

---

## Pricing Reference Notes

Include at the end of every quote:

> **Pricing notes:** All prices are UK 2025/26 estimates based on national average trade rates and builders' merchant prices. Prices vary significantly by region (London +20-40%, South East +10-20%). Material prices fluctuate -- always get supplier quotes for accurate costs. Labour rates vary by experience, qualifications, and local market conditions.

---

## Quality Rules

1. **Be specific.** List actual materials with sizes and quantities, not vague categories.
2. **Show your working.** State dimensions, quantities calculated, and assumptions made.
3. **Use ranges.** Every price should be a low-high range reflecting real market variation.
4. **Don't pad.** Only include costs genuinely relevant to the described job.
5. **Flag unknowns.** If something cannot be estimated without a site visit (e.g. ground conditions for foundations), say so explicitly.
6. **Separate supply and fit.** If the client is supplying their own kitchen/bathroom/materials, clearly separate supply costs from fitting costs.
7. **Include the client document.** Every quote must include both the detailed breakdown (for the builder's internal use) and the client-ready quote document.
