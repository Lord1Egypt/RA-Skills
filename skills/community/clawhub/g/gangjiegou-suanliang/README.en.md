# Steel Tonnage Takeoff (gangjiegou-suanliang)

**[English](./README.en.md) | [中文](./README.md)**

**v0.4.0** · Formal quantities are loaded from `lis-skill-bus` by `contract_id`; the skill converts the `cad-file-reader` steel contract into a section spectrum, tonnage estimate band, and member ledger without reading drawings.

The formal recognition path is fixed: `cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`. This skill never reads DWG/DXF/PDF and does not provide a second recognition path that bypasses `cad-file-reader` or `lis-skill-bus`. `--steel`/a positional file path is a manual entry and requires explicit `--allow-manual`; it is never a formal quantity.

## Check availability first

Installing this skill alone does **not** install its prerequisites. After a marketplace install, run:

```bash
python3 scripts/steel_tonnage.py --check-deps
```

- Both found: exit 0; the formal recognition path is ready.
- Either missing: exit 20 (no cad-file-reader) or 21 (no lis-skill-bus), an explicit missing-dependency message, and one copyable install command. A DWG cannot be recognized. A file contract can still be calculated only with explicit `--allow-manual`; the result has `final_quantity=false` and is not a formal quantity.
- `manifest.json` declares `cad-file-reader>=0.41.0 (with cad-file-reader:packs/steel-geometry)` and `lis-skill-bus>=0.1.11` under `requires.skills`.

## What it does

- Consumes `cad-steel-geometry/v1` and emits `cad-steel-tonnage/v0.2` as JSON, Markdown, and CSV.
- Uses geometry formulas for fully dimensioned H sections, tubes, rectangular tubes, angles, C/Z purlins, channels, and plates.
- Uses GB/T 706 theoretical weights for numbered hot-rolled channels `[5`~`[40` and I-beams `I10`~`I63`, including a/b/c variants.
- Reports tonnage by steel grade from `materials[]`; members without grade evidence stay in `unknown_grade`.
- Builds a member-code merge ledger with instance counts, section sets, explicit lengths, and coordinates; conflicts go to review.
- Counts high-strength bolts, bolts, anchor bolts, studs, connection plates, and stiffeners from `connections[]`; only connection plates with thickness-width-length or thickness-area evidence enter tonnage.
- Reports primer, topcoat, hot-dip galvanizing, and fireproof-coating areas from `finishes[]`; missing area/range stays `unavailable`, and fire ratings are not inferred.
- Uses explicit member lengths first; otherwise sums steel-layer drawn segments. With no length evidence it emits the section spectrum only.
- Prefers the member-level ledger for the headline total; allocation is a draft reference only. The reported band is `-15%~+15%` with `final_quantity=false`.

## Two total-tonnage fields

| Case | `total_t` | `total_t_allocated_estimate` |
|---|---|---|
| Every member code has an explicit length and exactly one weight-bearing section | Sum of `member_merge[].tonnage_t`; `total_basis=member_level` | Still retained for draft comparison |
| Member ledger incomplete (missing length, missing section, or multi-section conflict) | Weighted allocation by `unit weight x label count`; `total_basis=allocated_estimate`; prominent warning at the top of the report | Same as `total_t` |
| No length or no weight-bearing section | Empty array | Empty array, or connection plates only |

`member_level_note` explains why member-level was not used. Only when `total_basis=member_level` do the report and CSV label `total_t` as “recommended”; an allocated fallback is labelled “draft, not an answer” and keeps the `total_t_allocated_estimate` qualifier.

## Quick start

### 1. Formal recognition path

```bash
# Probe prerequisites first; exit 20/21 when a dependency is missing
python3 scripts/steel_tonnage.py --check-deps

# Reuse a matching contract when available; no second drawing parse
bash scripts/gangjiegou_statesync.sh pull --project PROJECT

# Otherwise cad-file-reader performs the only drawing recognition
bash skills/cad-file-reader/scripts/cad_scan.sh drawing.dwg \
  --with-mtext --with-insert --with-geom --with-geom-layer \
  --detail-json detail.json --format json -o cad-scan

bash skills/cad-file-reader/scripts/cad_steel_geometry.sh \
  detail.json --out-dir steel-geometry

# Publish the recognition contract through the bus
bash skills/cad-file-reader/scripts/cad_statesync.sh push \
  --entry-file steel-geometry/detail.steel.json --project PROJECT --specialty steel

# Validate first; structural errors exit 2 and never produce tonnage
python3 scripts/steel_tonnage.py \
  --validate steel-geometry/detail.steel.json --report contract-health.json

# Formal quantity: load by contract_id from the bus and write JSON/MD/CSV
# contract_id comes from the push output or a bus pull result
python3 scripts/steel_tonnage.py \
  --from-contract <contract_id> --project PROJECT --out-prefix steel-tonnage
```

### 2. Load a formal contract from the bus

```bash
python3 scripts/steel_tonnage.py \
  --from-contract <contract_id> --project PROJECT --out-prefix /tmp/steel-tonnage
```

This is the formal-quantity entry, not a second recognition path. The contract must be produced by the formal chain and stored by `lis-skill-bus`. Saving a bus artifact to a local file and passing it through `--steel` forces the run into manual mode.

### 3. Manual contract (supported fallback)

When the recognition layer is unavailable, constructing `*.steel.json` by hand is supported:

```bash
python3 scripts/steel_tonnage.py --validate examples/minimal.steel.json
python3 scripts/steel_tonnage.py \
  --steel examples/minimal.steel.json --allow-manual --out-prefix /tmp/minimal-ton
```

`examples/minimal.steel.json` is the minimum sample. `examples/README.md` documents required fields, section-to-member matching, millimetre coordinates, and `$`-nested layer names.

### 4. Sensitivity when lengths are missing

```bash
python3 scripts/steel_tonnage.py \
  --from-contract <contract_id> --project PROJECT --out-prefix steel-tonnage \
  --length-scenario 4.5 --length-scenario 6 --length-scenario 9
```

`length_scenarios[]` compares uniform member-length assumptions and is explicitly labelled “not a result”.

## Common options

| Option | Purpose | Exit status |
|---|---|---|
| `--check-deps` | Probe `cad-file-reader` / `lis-skill-bus` only; print one install command when missing | 0 when ready, 1 when missing |
| `--validate <json>` | Contract health check only: fields, unmatched members, count-only sections, length evidence, dependencies | 0 when calculable, 2 on structural errors |
| `--report <json>` | Write the health report as `cad-steel-contract-health/v1` | Follows `--validate` |
| `--from-contract <id>` | Formal entry: load the contract from `lis-skill-bus` by `contract_id` | 0 on success; missing/source/version errors 1/3/4 |
| `--project <project>` | Bus project used by `--from-contract` | Follows `--from-contract` |
| `--steel <json>` | File/manual contract entry; requires `--allow-manual` | 0 on success; 3 without the flag |
| `--allow-manual` | Explicitly permit a file contract; forces `provenance=manual`, `formal_ledger_eligible=false` | Follows the file entry |
| `--out-prefix <prefix>` | Output `.json/.md/.csv` prefix | 0 on success |
| `--length-scenario <m>` | Repeatable length-sensitivity scenario | 0 on success |

## Caliber notes

| Item | Current behavior |
|---|---|
| Estimate band | `±15%`, for draft review |
| H sections | 4-part sections use formulas; 2-part H sections are count-only |
| Channels | Fully dimensioned sections use formulas; numbered sections use GB/T 706 |
| I-beams | Numbered `I10`~`I63`, including a/b/c, use GB/T 706 |
| Length | `explicit` first, `drawn` second, `none` produces no tonnage |
| Headline total | `member_level` when the ledger is complete; otherwise `allocated_estimate` draft |
| Grades | Evidence-based Q235/Q345/Q355/Q390/Q420/Q460/S235/S355/A36/16Mn; `unknown_grade` and `mixed_grade` are never defaulted |
| Member merge | Same-code instances merged; category/system conflicts, missing code, or no section go to review |
| Coordinates | `members[].x/y/z/rotation` in mm; missing coordinates set `location_status=missing` |
| Connections | Six categories; explicit quantities first, otherwise label counts with review |
| Finishes | Four area categories; missing area/range is `unavailable`; no fire-rating inference |
| Hoisting allowance | `allowance_advice` suggests 3%/5%/8%, never folded into `total_t` |
| Geometry closure | `geometry_closure` from the recognition layer is passed through as `geometry_closure_check`; this skill does not scan drawings |

## Outputs

Each calculation writes three files:

- `*.json`: `cad-steel-tonnage/v0.2`, with `final_quantity`, length basis, grade bands, member ledger, connection/finish ledgers, review items, section bands, section spectrum, and count-only sections.
- `*.md`: readable review report with recommended total, draft allocation reference, length basis, prerequisite status, and review items at the top.
- `*.csv`: total band, section bands, member ledger, connection/finish summaries, and section spectrum.

Key fields include `provenance`, `contract_id`, `source_sha256`, `contract_sha256`, `reader_version`, `formal_ledger_eligible`, `run_manifest`, `length_basis`, `length_used_m`, `rows`, `spec_rows`, `only_count`, `total_t`, `total_basis`, `total_t_member_level`, `total_t_allocated_estimate`, `member_merge`, `length_scenarios`, `allowance_advice`, `geometry_closure_check`, `prerequisites`, `input_evidence`, and `summary`.

When `steel_geometry[]`, `connections[]`, or `finishes[]` is empty, the report says “no evidence in input” so it is not confused with “not implemented”.

## What it does not do

- It does not scan DWG, DXF, DWT, or PDF files. Drawing recognition belongs to `cad-file-reader`.
- It is not for deepened design, fabrication detailing, cutting lists, settlement, formal pricing, or completion measurement.
- It does not fill gaps with defaults: missing length/width/thickness, out-of-table sections, or unknown section types are count-only and remain subject to human review.
- Not supported yet: tonnage for connections other than connection plates, weld tonnage, exact member-to-section mapping and net quantities, grade-based unit-weight adjustment, curved or multipart geometry length, 3D-model coating areas, and fire-rating inference.

## Dependencies

- Python 3.10+; the main calculation entry uses only the standard library.
- Formal recognition: `cad-file-reader>=0.41.0` (with `cad-file-reader:packs/steel-geometry`) and `lis-skill-bus>=0.1.11`.
- Existing or manual contracts: neither skill is required for calculation, but a file entry requires explicit `--allow-manual` and is not a formal quantity. `--from-contract` requires `lis-skill-bus`.

## Validation

```bash
python3 tests/test_entry_gate.py
cd scripts/tests
python3 -m unittest test_steel_tonnage
```

Current v0.4.3 includes **35 entry-gate assertions + 49 synthetic-data unit tests**. The gate tests cover `--check-deps`, manual exit 3, `--allow-manual` downgrade, forged-reader rejection, missing bus contract, `cad-contract/v0` rejection, and a valid reader contract. The 49 existing tests cover unit-weight formulas, GB/T 706 lookups, both length bases, no-length fallback, contract rejection, duplicate codes, grade bands, `unknown_grade`, connection-plate tonnage and grade residuals, member-merge review, connection categories, finish fallback, member/allocation totals, coordinate passthrough, `--validate`, and length scenarios.

Admission boundary: `provenance`/`contract_id` are not cryptographic proof. The current gate prevents accidental bypass, not well-formed forgery. Real verification still needs reader/bus signatures or a `contract_id` whitelist.

Smoke test:

```bash
cd ../..
python3 scripts/steel_tonnage.py --validate examples/minimal.steel.json
python3 scripts/steel_tonnage.py \
  --steel examples/minimal.steel.json --allow-manual --out-prefix /tmp/minimal-ton
```

## License

`CC-BY-NC-SA-4.0`. Commercial use requires separate written permission from the author; see `LICENSE.md`.
