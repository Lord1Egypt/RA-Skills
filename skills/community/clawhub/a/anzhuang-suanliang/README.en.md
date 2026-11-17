# Installation/Mechanical-Electrical-Plumbing (MEP) Rough Quantity Takeoff

> anzhuang-suanliang (anzhuang-suanliang) v0.4.38 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
Extracts MEP rough-quantity working papers and material-plan drafts from installation DWG/scanned indexes. It groups pipes by circuit and size, expands wire cores and reserved lengths, and estimates cable, cable tray, water/supply, sprinkler, supports/hangers and equipment counts for budgeting, material planning, drawing-review cross-checks and professional-software reconciliation.

## When to use it
Use when you need MEP rough quantities from building drawings without CAD software. It does NOT replace shop drawing/detailing, material scheduling/fabrication, settlement, or pricing, and never outputs RMB amounts.

## Quick start
```bash
bash scripts/mep_scan.sh plan.dwg --out scan.json
bash scripts/mep_plan.sh --scan scan.json --out-prefix out
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3.10+; requires cad-file-reader (auto-detected and auto-installed to vendor on first run, checksum-verified) and openpyxl for XLSX output.

## Privacy
Runs fully locally; DWG bytes are never uploaded.

## Boundaries / limitations
Estimates only; must be cross-checked with contracts, local rules, design files and professional software. Review items are flagged for human confirmation.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
