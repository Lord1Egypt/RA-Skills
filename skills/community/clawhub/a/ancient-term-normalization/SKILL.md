---
name: ancient-term-normalization
description: |
  Normalises recognised characters or words from ancient manuscripts and excavated texts by mapping them to standardised forms. Use this skill after OCR or character recognition to expand ambiguous characters into sets of aliases (e.g. 荆 → 楚, 荆楚). The skill reads a JSON file of recognised characters and produces a JSON file of normalised terms.
license: MIT
compatibility: |
  Requires Python 3.10+ and PyYAML. Scripts run in a sandbox environment with read/write access to the workspace. No network access is required.
allowed-tools: Bash(python:*), Bash(jq:*)
metadata:
  author: ai4s
  version: "1.0.0"
  domain: humanities
---

# Ancient Term Normalisation Skill

## When to use

Use this skill when you have a list of characters or terms recognised from manuscripts and want to generate possible aliases, alternative spellings or historical equivalents. This is useful for search and retrieval because many names and states have variant forms in historical sources.

## How it works

1. **Input** – Provide a path to a JSON file containing recognised characters and their confidence scores. The input must follow the schema defined in `assets/schemas/recognized_chars.schema.json`.
2. **Lookup** – The script loads a YAML file of alias rules (`assets/data/historical_aliases.yaml`) where each key maps to a list of standardised forms. If a character is absent from the mapping, it is preserved as its own normalised form.
3. **Output** – A JSON file is written to the `term_normalisation/` folder in the workspace. Each entry contains the original character, the list of normalised forms, the entity type, notes and the original confidence score. The output conforms to `assets/schemas/normalized_terms.schema.json`.

## Files produced

Outputs reside under `term_normalisation/` in the workspace:

- `normalized_terms.json` – list of normalised term objects.

## References

- See `references/REFERENCE.md` for input and output schema details.
- See `assets/data/historical_aliases.yaml` for the mapping of historical names to standardised forms.