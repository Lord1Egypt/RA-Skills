# embedded-solution

Recommend embedded system solutions: chip selection, BOM design, vendor
comparison, and reference design matching across multiple semiconductor vendors.

## What this skill does

When you ask a question about embedded systems — chips, MCUs, BLE/WiFi/LoRa
SoCs, sensor selection, BOM design, reference designs — this skill:

1. Checks its catalogue of chip indexes (`references/semiconductor-vendor/<Vendor>/product_families.md`)
2. Cross-references application-solution templates (`references/application-solution/<topic>/solution.md`)
3. Returns **top 3 candidates + comparison table** by default (not a single pick)
4. Cites vendor URLs for every recommendation
5. Says **"not verified"** for any parameter it cannot confirm against official sources

It does **not** fabricate part numbers, specs, prices, or stock counts.

## Quick start

```text
You: "I'm designing a smart ring with BLE and 1-week battery life."

Skill: (asks Step 5 clarifying questions — battery capacity, size, sensor set, ...)
You: (answers)

Skill: (returns top 3 BLE SoC candidates + comparison table + trade-offs,
        each linked to vendor URL and marked with verification status)
```

## When this skill triggers

✅ Triggers for: BLE SoC selection, WiFi+BLE combo, BOM design, vendor
comparison, datasheet parameter verification, application-solution matching,
matter/thread/lorawan design, industrial IoT, smart home/ring/glasses/lock
design, motor control BOM.

❌ Does NOT trigger for: pure software/learning ("how to write Hello World
in Rust"), web/cloud/database questions, math without hardware context.

See [`SKILL.md`](SKILL.md) for full trigger conditions and workflow.

## Install

```bash
clawhub install embedded-solution
```

Public release mode (no `specs/`). Maintainers / dev clones with
`git submodule update --init` get the full private spec database — see
[`SKILL.md`](SKILL.md) → *Privacy / Publishing Notes* > *Maintainer note*.

## Repository layout

```
embedded-solution/
├── SKILL.md                                       # Read this first — the whole skill
├── README.md                                      # This file
├── scripts/
│   ├── update_specs.py                            # Extract specs from datasheets (maintainer)
│   ├── build_application_index.py                 # Regenerate INDEX.md (maintainer)
│   └── check_no_specs_dead_refs.sh                # CI guard: scan for user-facing specs/ path refs
├── references/
│   ├── semiconductor-vendor/<Vendor>/             # Per-vendor chip indexes (8 vendors)
│   │   ├── product_families.md                    # The canonical "what does this vendor offer" file
│   │   └── system-solutions/                      # Single-vendor reference designs
│   ├── application-solution/                      # Multi-vendor application BOM templates
│   │   ├── INDEX.md                               # Auto-generated catalog
│   │   ├── smart-ring/solution.md
│   │   ├── smart-glasses/solution.md
│   │   └── robot-gripper/solution.md
│   └── testing/                                   # Regression test fixtures
│       ├── README.md
│       ├── evaluation-rubric.md
│       ├── fixtures/                              # 7 user prompt templates
│       └── expected-outputs/                      # Structural skeletons per fixture
└── specs/                                         # PRIVATE — git submodule, not shipped
```

## For maintainers

### Adding a new vendor

1. Create `references/semiconductor-vendor/<VendorName>/product_families.md`
   following the existing format (see `Renesas/product_families.md` for full example).
2. Add at least one product URL and verification status.
3. Run `bash scripts/check_no_specs_dead_refs.sh` to verify no broken paths.

### Adding a new application-solution

1. Create `references/application-solution/<topic>/solution.md`.
2. Follow the structure of `smart-ring/solution.md` (Overview / BOM Candidates
   / Reference Designs / Selection Matrix / Verification Status / Caveat).
3. Run `python3 scripts/build_application_index.py` to refresh INDEX.md.

### Adding a regression test fixture

1. Add `references/testing/fixtures/<NN>-<topic>.md` with verbatim prompt +
   workflow path + acceptance criteria.
2. Add `references/testing/expected-outputs/<NN>-<topic>.expected.md` with
   structural skeleton (table headers, citation anchors, anti-patterns).
3. Optionally extend `evaluation-rubric.md` if a new scoring axis is needed.

## Testing

7 regression fixtures cover the main SKILL.md workflow paths. Run manual
evaluation by feeding a fixture's "Input prompt" to the skill and scoring
the response against `evaluation-rubric.md` (5 axes × 5 pts = 25 max,
pass = 20+).

```bash
# Run the dead-reference guard
bash scripts/check_no_specs_dead_refs.sh

# (Optional) Run all 7 fixtures against the skill and score manually
# See references/testing/README.md for the script template
```


## Contributing — specs/ is open

Starting from **v0.6.0** (2026-07-05), the previously-private `specs/` directory is released alongside the skill. The YAML files contain field-level extraction of official vendor datasheets, plus provenance (`link_status`) for every entry.

### What this unlocks

- **Transparent provenance** — every numeric spec the skill cites can be traced to its `link_status` field and the underlying datasheet page.
- **Community contribution** — PRs adding new chips, fixing stale fields, or upgrading `link_status` from `placeholder_*` → `verified_*` are welcome.
- **Cross-verification** — a second pair of eyes catches transcription errors that one person would miss.

### What counts as a valid entry

- Every numeric field must trace to a **specific page** in a **vendor official** PDF (or vendor URL). The `link_status` field documents this provenance.
  - `verified_*` — the field was extracted from the linked PDF and matches the spec table.
  - `placeholder_*` — the field is a TODO. **Never treat a placeholder as verified.**
- Per-field tier citations are encouraged: see `SKILL.md` Step 4 for the 4-tier Search Priority.

### Contribution workflow

```bash
# 1. Pick a missing or stale chip in specs/<Vendor>/<Part>.yaml
# 2. Pull its datasheet into embedded_dev/<vendor>/datasheet/<Part>_datasheet.pdf
# 3. Run scripts/update_specs.py to extract fields
# 4. Run scripts/verify_yaml_vs_datasheet.py to check match rate
# 5. Open a PR — review focus is provenance, not opinions
```

### Currently covered vendors

See `specs/<Vendor>/` for the current chip roster. Major vendors with verified entries include Espressif, GigaDevice, NXP, Nordic, Renesas, SGMicro, ST, Silergy, SiliconLabs, TI, WCH. Missing a vendor? Open an issue first to discuss the YAML schema for that vendor's fields.

Welcome — and thanks for making this skill more reliable, one chip at a time. ✨


## License

MIT. See SKILL.md header for full license.

## Contributing

Issues and PRs welcome. For major changes (new vendor, new application domain,
new top-level SKILL.md section), please open an issue first to discuss.

---

**Full skill definition:** [`SKILL.md`](SKILL.md)
**Test suite:** [`references/testing/`](references/testing/)
**Evaluation rubric:** [`references/testing/evaluation-rubric.md`](references/testing/evaluation-rubric.md)
