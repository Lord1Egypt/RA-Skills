---
name: fill-xfa
description: "Fill XFA (Adobe LiveCycle) PDF forms programmatically. Use when working with .pdf files that have Form: XFA (check with pdfinfo). Standard tools like pdftk, pypdf, PyPDF2 cannot fill XFA forms — this skill extracts the embedded XML, sets field values, and writes back. Triggers: filling PDF forms, XFA forms, Adobe LiveCycle forms, form.fdf alternatives, Formular ausfüllen, PDF befüllen, Behördendrucke,-government forms"
---

# Fill XFA PDF Forms

Fill any Adobe LiveCycle XFA form from the CLI. Solves a gap that standard PDF tools cannot address.

## Why This Exists

XFA forms (Form: XFA in pdfinfo) embed data as XML inside the PDF, not as standard AcroForm fields. Tools like `pdftk`, `pypdf`, and `PyPDF2` silently fail or produce empty output. This script modifies the embedded XFA XML directly.

## Prerequisites

```bash
pip install pikepdf
```

## Quick Start

```bash
SCRIPT="<skill_dir>/scripts/fill_xfa.py"

# 1) Verify the form is XFA:
pdfinfo form.pdf | grep Form  # Should show: Form: XFA

# 2) Discover field names:
python3 "$SCRIPT" fields form.pdf

# 3) Fill from JSON:
python3 "$SCRIPT" fill form.pdf -o filled.pdf -d data.json
```

## Commands

### `fields` — List Data Fields

```bash
python3 "$SCRIPT" fields form.pdf
```

Outputs sorted field names with current values and duplicate counts.

### `fill` — Set Field Values

Three input methods — combine freely:

```bash
# Repeatable --set flags:
python3 "$SCRIPT" fill form.pdf -o out.pdf \
  --set "Eigentümer_Name=Müller" \
  --set "Eigentümer_Vorname=Anna" \
  --set "PLZ=84424"

# JSON file:
python3 "$SCRIPT" fill form.pdf -o out.pdf -d fields.json

# Stdin pipe:
printf '{"Name":"Müller","Vorname":"Anna"}' | \
  python3 "$SCRIPT" fill form.pdf -o out.pdf --stdin
```

## JSON Data Format

```json
{
  "Feldname": "Wert",
  "Eigentümer_Name": "Müller",
  "Datum": "2026-05-05"
}
```

Field names must match the XML element names in the form (discover with `fields`).

## Duplicate Fields

Some forms reuse field names (e.g., multiple `Textfeld1`). Two modes:

- **Same value everywhere:** `--set Textfeld1=3` sets all occurrences to "3"
- **Different values per occurrence:** Pass an array: `{"Textfeld1": ["A", "B", "C"]}` distributes values across duplicates (first field gets "A", second gets "B", etc.)

## Limitations

- Only works with XFA forms — verify first: `pdfinfo form.pdf | grep Form`
- Form must not be password-protected
- Namespace restoration preserves only the first `xmlns:*` declaration (rarely matters)
- Some forms require manual wet-ink signature after filling

## Common Use Cases

- Government registration forms (German: Behördendrucke, Landkreis forms)
- Utility company forms (waste collection, water/electricity)
- School enrollment applications
- Any Adobe LiveCycle Designer form downloaded from official websites

## Example: German Waste Bin Registration

```bash
# Discover fields:
python3 "$SCRIPT" fields tonnenanmeldung_blank.pdf

# Fill from JSON (pipe to stdin):
python3 "$SCRIPT" fill tonnenanmeldung_blank.pdf -o tonnenanmeldung_filled.pdf --stdin <<'EOF'
{
  "Neuantrag": "1",
  "Eigentümer_Name": "Müller",
  "Eigentümer_Vorname": "Anna",
  "Eigentümer_Straße": "Hauptstraße",
  "Eigentümer_Straße_Nummer": "5",
  "Eigentümer_PLZ": "84424",
  "Eigentümer_Ort": "Isen",
  "Eigentümer_seit": "2026-01-15",
  "Grundstück_Straße": "Beispielweg",
  "Grundstück_PLZ": "85435",
  "Grundstück_Ort": "Erding",
  "Grundstück_Haus_Nummer": "12",
  "Textfeld1": "3",
  "Restmüll_ab": "07/2026",
  "Zugang_80_l": "1",
  "Bio_Zugang_80_l": "1",
  "Papier_Zugang_240_l": "1",
  "Kontoinhaber_Name": "Müller, Anna",
  "Kontoinhaber_Straße": "Hauptstraße 5",
  "Kontoinhaber_Ort": "84424 Isen",
  "Kontoinhaber_Kreditinstitut": "VR-Bank",
  "Kontoinhaber_IBAN": "DE",
  "Kontoinhaber_IBAN_Nummer": "1234567890",
  "Kontoinhaber_BIC": "GENODEF1XXX",
  "Datum": "2026-05-05"
}
EOF
```
