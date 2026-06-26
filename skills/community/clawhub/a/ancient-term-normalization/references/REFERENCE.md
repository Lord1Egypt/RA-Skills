# Reference Documentation for Ancient Term Normalisation

This document expands on the information in `SKILL.md`, describing the expected inputs, outputs and internal behaviour of the ancient-term-normalization skill.

## Input

The input is a JSON file containing a list of recognised characters or strings and optionally their recognition confidence. The file must have the following shape (see also `assets/schemas/recognized_chars.schema.json`):

```json
{
  "recognized_chars": [
    {"text": "荆", "confidence": 0.72},
    {"text": "隐公", "confidence": 0.81}
  ]
}
```

Each entry in the list must include a `text` field. The `confidence` field is optional but recommended.

## Alias mapping

The mapping of recognised characters to their standardised forms is defined in the YAML file `assets/data/historical_aliases.yaml`. Each top‑level key represents an original term (exact match) and contains:

- `aliases` – a list of canonical forms for retrieval.
- `type` – the type of entity (e.g. `state_name`, `ruler_name`, `excavated_text`).
- `note` – a short explanatory note to provide context.

If a recognised term is not present in the alias mapping, it will be normalised to a list containing only itself and its type will be `unknown`.

## Output

The output JSON file (stored at `term_normalisation/normalized_terms.json`) has the following shape (see `assets/schemas/normalized_terms.schema.json`):

```json
{
  "normalized_terms": [
    {
      "original": "荆",
      "normalized": ["楚", "荆楚"],
      "type": "state_name",
      "note": "先秦文献中常以“荆”指称楚。",
      "confidence": 0.72
    },
    {
      "original": "隐公",
      "normalized": ["鲁隐公"],
      "type": "ruler_name",
      "note": "可作为鲁国纪年线索。",
      "confidence": 0.81
    }
  ]
}
```

Each entry retains the original recognition confidence value for downstream weighting. Developers may extend the schema to include additional metadata as needed.