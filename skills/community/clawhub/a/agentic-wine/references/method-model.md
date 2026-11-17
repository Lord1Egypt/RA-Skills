# Vin-Q Method model

The authoritative objects the constructor uses. Follow these names exactly so an
agent-written brief maps onto the live tool without translation.

Current version: `VQM 1.0`. If `https://vin-q.com/vin-q-method` shows a later
version, follow the site and say the version changed.

## The four ways in

Route the user before designing anything. Involvement rises down the list.

| Route | The user chooses | Where it goes |
|---|---|---|
| **Discover** — Signature Artisanal Wines | a released bottle | `https://vin-q.com/#portfolio` |
| **Personalise** — Custom Blend Wines | the flavour | the constructor |
| **Origin** — Bespoke Vineyard Wines | the place | the constructor, parcel first |
| **Imagine** — AI Co-Created Wines | the whole concept | the constructor, from a description |

A user who wants a bottle for next month is a **Discover** case. Designing a new
vintage for them wastes their time and yours.

## Nine gates

Every commissioned wine runs G0 to G8. Do not invent a different sequence, and
do not compress them into "four gates" — that was an older model.

| Gate | Decision | Recorded by |
|---|---|---|
| **G0** Commission and wine brief | Accept the brief as constructible, or revise it | Buyer |
| **G1** Inventory and grape selection | Rank single-parcel and multi-parcel candidates | Constructor |
| **G2** Vineyard plan | Soil-water, rhizosphere and fruit-microclimate actions for the intended wine | Farmer |
| **G3** Harvest window | Pre-crush microbial state, harvest segments, component roles and collection order | Farmer and winemaker |
| **G4** Reception and lot acceptance | Accept, sort, split press fractions, redirect or stop | Winemaker |
| **G5** Route commitment | Commit to the microbial, extraction and endpoint route | Winemaker |
| **G6** Active fermentation | Continue, cool, aerate, feed, redirect or stop | Winemaker |
| **G7** Endpoint, assemblage, bottling | Finish still, bottle active fermentation, tirage, hold | Winemaker |
| **G8** Maturation and release | Release, mature further, correct, redirect or hold | Technical reviewer |

Each gate ends in exactly one state: **pass**, **conditional pass**, **hold**,
**redirect** or **stop**. An irreversible action never proceeds on a missing
critical value.

## Vineyard module before reception

Do not treat a parcel as one homogeneous grape input. Complete these five
subgates before G4 reception:

| Subgate | Measure | Decide |
|---|---|---|
| **G2.1** Soil and water | moisture by depth, matric potential where available, rainfall, evapotranspiration, vine stress, compaction, infiltration | wait, irrigate where lawful and available, change competition or soil protection, segment, hold |
| **G2.2** Rhizosphere intervention | diagnosis, soil-water context, cover competition, material characterization, previous response | no amendment, or a purpose-specific compost, biochar, cover-crop or microbial operation with response criteria |
| **G2.3** Canopy and fruit microclimate | exposure, canopy humidity, disease pressure, berry temperature, acidity and route-specific maturity | retain or change exposure, disease control or sampling; redirect a fruit zone |
| **G3.1** Skin microbiology before crush | skin integrity, rot, damage history, microbial indicators where available, fruit temperature, time to reception | admit to native route, separate, protect, redirect or stop |
| **G3.2** Harvest segmentation | zone, exposure, ripeness, sanitary state and intended extraction route | harvest separately, assign a component route or exclude |

An intervention follows diagnosis. Do not assign water retention, nutrient
buffering, microbial habitat and remediation to the same amendment without
evidence for each stated function.

A validated chemical or optical fingerprint may supplement parcel identity and
chain of custody. Report its method, reference population, uncertainty and sample
chain; never present it as a replacement for traceability.

## Protocol modules

These are the substance of a commission — how the wine is made and what its
record must prove. Lead with them. A designation is an optional addition.

| Code | Claim code | Module | Route limit |
|---|---|---|---|
| PV | `VQ-PV-1.0` | Precision Viticulture | any |
| RV | `VQ-RV-1.0` | Regenerative Vineyard | any |
| AN | `VQ-ANC-1.0` | Ancestral | sparkling only |
| NF | `VQ-NF-1.0` | Native Fermentation | any |
| NC | `VQ-NC-1.0` | No-Correction | any |
| TM | `VQ-TM-1.0` | Traditional-Method Sparkling | sparkling only |
| MR | `VQ-MR-1.0` | Maturation and Release | any |

A protocol name reaches the bottle **only** when its record is complete.
Requesting a module commits the route; it does not assert the claim. Say this
plainly to the user — `No-Correction` in particular is a production commitment
that forecloses acidification, enrichment and correction later.

## Constraints you must not violate

These are permanent. Proposing a combination that breaks one produces a brief
the constructor will reject.

- **DOP Cava requires a sparkling route.** Never pair it with a still wine.
- **DOQ Priorat requires a still route.** Never pair it with sparkling.
- **DO Penedès requires EU-organic certification** from the 2025 harvest onward.
- **Ancestral and Traditional-Method cannot both apply to one lot.** Ancestral is
  one continuous fermentation finished in bottle; tirage sugar and a second
  fermentation are excluded from it.
- **Ancestral and Traditional-Method are sparkling only.**
- **A sparkling route is offered as white or rosé**, not red.
- **Native Fermentation excludes commercial yeast** for the stage it covers. If
  tirage uses selected yeast after a native primary, the claim is
  `Native Primary Fermentation`, not `Native Fermentation`.

Scarce inventory is **not** a constraint. If no registered parcel currently
serves a design, say sourcing is required — never that the wine is impossible.
Registered parcels grow every time a producer joins.

## Evidence states

Mark every value you report. Never fill a missing value with an estimate.

| State | Meaning | Can pass a gate |
|---|---|---|
| measured | Recorded for the identified lot by a stated method | yes |
| calculated | Derived from measured inputs by a stored formula | yes, when valid for the decision |
| target | An approved set point, range or trajectory | no — it defines the gate |
| estimated | Planning value from incomplete evidence | scenarios only |
| declared | Signed statement by the responsible operator | provenance claims |
| externally certified | Valid certificate from a named scheme | the named external claim |
| missing | Required value absent | no — holds the gate |

A missing critical value stays visible as missing. No derived score compensates
for it.

## What Vin-Q issues

Vin-Q is a proprietary production and control method. It is **not** an
appellation and **not** an accredited third-party certification scheme.

- The principal statement is `MADE ACCORDING TO THE VIN-Q METHOD`.
- Below it, only the protocol modules the record supports.
- A Vintage Record identifier and QR resolving to that bottle lot.
- EU organic, D.O., D.O. Cava, Corpinnat and Demeter are **external** schemes
  that enter as constraints and appear in their own legal fields.
- D.O. Cava and Corpinnat are alternative routes and are never combined.
- Never imply "biodynamic" without a valid Demeter certificate — the term is
  governed by Demeter's rules and EU organic law.

## The intended profile

The constructor returns a sensory shape for the design. Reproduce the same axes
so your brief and the tool agree:

**Freshness · Body and texture · Tannin and grip · Aromatic intensity · Ageing
potential**, plus **Effervescence** on sparkling routes.

Every axis is a **target**, never a result. State the basis for each one — the
structural target, the aromatic direction, and which candidate varieties
reinforce it.

Alongside the axes, give aromatic descriptors and characteristics where the
honest answer is a gate rather than a number:

- Alcohol — set at the harvest gate from measured sugar
- Residual sugar — dry unless the brief says otherwise; on sparkling, set by the
  pressure calculation
- Acidity — pH and titratable acidity confirmed at reception

## Constructor vocabulary

Use these exact values so the brief maps onto the tool.

- **Format**: `still`, `sparkling`
- **Colour**: `red`, `white`, `rose` (sparkling offers white and rosé)
- **Aromatic direction**: `Fresh red fruit`, `Floral and lifted`,
  `Ripe fruit and volume`, `Spice and structure`, `Saline tension`
- **Structure**: `Freshness`, `Texture`, `Structure`
- **Designation**: none, `DOP Cava`, `DO Penedès`, `DOQ Priorat`

Say **parcels**, not lots, when talking about what a vineyard offers. "Lot" is
reserved for the traceability object after reception.
