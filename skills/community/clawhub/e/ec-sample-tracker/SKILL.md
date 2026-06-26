# ec-sample-tracker-1.0.0 — Sample Tracker for Electrochemistry Labs

Track physical samples from synthesis through every characterization result. Connect samples to their storage locations, synthesis records, and all associated data files (LSV/CV/EIS/XRD/SEM/TEM etc.).

## Usage

```bash
ec-sample-tracker <command> [options]
```

## Commands

- `add` — Register a new sample
- `list` — List samples with filters
- `status` — Show sample status overview
- `link` — Attach data files or notes to a sample
- `search` — Search samples by name, tag, synthesis date, or property
- `log` — Log an experimental event (measurement, storage move, aging)
- `export` — Export sample records as CSV/JSON/Markdown
- `import` — Bulk import from CSV
- `dashboard` — Visual dashboard of sample inventory and status

## Sample Record Schema

```
sample_id       — Auto-generated (e.g. CAT-2026-0042)
name            — Sample name/label
synthesis_date  — YYYY-MM-DD
synthesis_method — hydrothermal / electrodeposition / impregnation / sol-gel / thermal decomposition / commercial
precursors      — Comma-separated list
substrate       — GC / Ti foil / Ni foam / FTO / ITO / Carbon paper / None
catalyst_load   — mg/cm² (if applicable)
target_reaction — OER / HER / ORR / CO2RR / other
tags            — Comma-separated tags
storage_location — fridge-4 / rack-A2 / desiccator-2 / given-out
owner           — Name
notes           — Free-text notes
status          — active / degraded / given-out / disposed / lost
```

## Link Types

- `ec` — LSV/CV/EIS/CP/CA files
- `xrd` — XRD data
- `sem` / `tem` — Electron microscopy
- `raman` — Raman spectra
- `xps` — XPS data
- `photo` — Sample photos
- `note` — Free-text notes
- `protocol` — Synthesis protocol PDF

## Configuration (config.yaml)

```yaml
lab_name: "Electrochemistry Lab"
id_prefix: "CAT"
next_id: 1
storage_locations:
  - fridge-4
  - rack-A2
  - rack-B1
  - desiccator-2
  - drawer-3
  - given-out
default_owner: "xray"
db_file: "samples.db"
data_root: "/home/xray/data"
```

## Dashboard

Generates a 4-panel PNG dashboard:
1. Sample count by status (pie chart)
2. Samples by reaction type (bar chart)
3. Storage location distribution (bar chart)
4. Recent activity log (text table)

## Examples

```bash
# Add a new sample
ec-sample-tracker add --name "NiFe-LDH/CF-2026-042" \
  --method hydrothermal --precursors "Ni(NO3)2,Fe(NO3)3" \
  --substrate "Ni foam" --load 2.1 --reaction OER \
  --tags "NiFe-LDH,hydrothermal,batch-42" \
  --storage fridge-4 --notes "Synthesized for OER stability test"

# Link characterization data
ec-sample-tracker link CAT-2026-0042 --type ec --file ~/data/oer_lsv_042.csv
ec-sample-tracker link CAT-2026-0042 --type xrd --file ~/data/xrd_042.asc

# Search samples
ec-sample-tracker search --tag NiFe-LDH --reaction OER
ec-sample-tracker search --synth-date-after 2026-03-01

# List all active samples
ec-sample-tracker list --status active

# Log an experimental event
ec-sample-tracker log CAT-2026-0042 --event "LSV cycling started" \
  --note "100 cycles in 1M KOH, 10 mA/cm²"

# Export all samples
ec-sample-tracker export --format markdown --output samples-report.md

# Generate dashboard
ec-sample-tracker dashboard --output sample-dashboard.png
```

## Database

Uses SQLite (`samples.db`) with tables:
- `samples` — Core sample records
- `links` — File/note attachments
- `events` — Timestamped experimental events
- `measurements` — Quantitative measurement results (overpotential, Tafel, ECSA, etc.)

## Output Files

- `samples.db` — SQLite database
- `samples.csv` — Full export
- `sample-dashboard.png` — Visual dashboard (300 DPI)
- `sample-YYYY-MM-DD.md` — Markdown report

## Use Cases

- Track which samples have LSV/CV/EIS data collected
- Find all samples from a specific synthesis batch or precursor combination
- Log degradation events and link to characterization
- Generate sample inventory for lab audits or paper supplementary
- Connect synthesis records to performance metrics
