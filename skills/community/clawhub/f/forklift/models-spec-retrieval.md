<!-- Copyright (c) 2026 Yang Pengfei / WeChat Official Account "Forklift Veteran". MIT License: see LICENSE.md. -->
# Model Specification Retrieval and Literal Extraction

Retrieve an official brochure, datasheet or specification page at answer time for every specific-model question. Do not store model specification tables locally. Use the latest verified revision for the correct region and configuration, and record the retrieval date.

## 1. Activation

Use this module for a named model's capacity, load centre, weight, mast/load chart, lift height, dimensions, aisle width, turning radius, battery, motor, charger, options, brochure request or disputed figure. General category questions belong in `knowledge.md` or `selection-guide.md`. Never substitute category averages for a named model.

## 2. Sources

Prefer: (1) manufacturer product page or PDF; (2) official regional subsidiary or authorized dealer; (3) manufacturer international site; (4) association/media reproduction; (5) B2B listing for cross-checking only. Select the correct regional variant using `brands.md` and `international-markets.md`.

Prefer documents with a brochure number, footer and revision date. Official sources prevail over reseller text. If only unofficial material exists, clearly label it "Unofficial reproduction; confirm against the current manufacturer brochure." The author's WeChat account is background, not sole evidence for exact specifications.

## 3. Workflow

1. Identify exact brand, model, suffix, series and market. Search alternative spellings without silently normalizing them. If no unique model is identifiable, ask for the nameplate/model/brochure rather than guessing.
2. Search manufacturer, official regional site and international site for an official PDF. Select the appropriate latest verified revision and cross-check other versions.
3. Read the PDF or official HTML specifications. If inaccessible, explain and request the document; never pretend it was read. Record document number, footer and date.
4. Extract field by field, preserving source names, figures, units, reference codes and model spellings. Do not convert, round, calculate or fill gaps. Record contradictions.
5. Disclose conflicts, follow the template, and include provenance and retrieval date.

## 4. Hard Extraction Rules

| Rule | Requirement |
|---|---|
| Official evidence | Manufacturer text is primary; secondary material is explicitly labelled |
| Literal extraction | Preserve figures, units, names and model spellings |
| Missing fields | Write "Not provided in source"; never borrow from another model or series |
| Contradictions | Show conflicting entries with page/field references and recommend manufacturer confirmation |
| Configuration columns | Keep capacity with sideshift, standard-fork weight and particular mast options distinct |
| Footnotes | Preserve markers; if explanation is absent, say "Footnote explanation not provided in source" |
| Advice | Label "Selection advice (not source text)" |
| Compliance | Preserve printed emission labels; verify legal claims via `standard-retrieval.md` |
| Provenance | Source URL + brochure number or "Not printed in source" + retrieval date |

If the user requests a calculation, place it in a separate "Calculation (not source text)" section with inputs and method. Never overwrite extracted values with derived values.

## 5. Search Templates

```text
<brand> <model> brochure pdf
<brand> <model> datasheet pdf
<brand> <model> specification sheet
<brand> <model> load chart mast residual capacity sideshift
site:<manufacturer-domain> <model> pdf
site:<regional-domain> <model> technical data
<brand> <model> standard equipment optional attachments
<brand> <capacity> tonne electric forklift model
```

Use the host's available search/fetch tools; prefer official PDF links. Social-media and reseller material require corroboration.

## 6. Template M

```text
Model: <all source spellings>
Brand / parent: <verified ownership>
Market and configuration: <region / variant>
Source: <official PDF or page URL>
Retrieved: <YYYY-MM-DD>
Brochure number: <literal number or Not printed in source>
Revision: <printed revision or Not printed in source>

Core specifications
| Parameter | Literal value | Source reference |
| Rated capacity | <figure and unit> | Q |
| Load centre | <figure and unit> | c |
| Service weight | <figure and unit> | <reference> |

Mast / lift
| Mast | Lift height | Lowered height | Free lift | Tilt | Capacity | Capacity with sideshift | Standard-fork weight |

Power / battery
| Item | Literal value | Reference |
Dimensions / aisle
| Item | Literal value |
Standard / optional equipment
| Item | Standard | Optional |

Source inconsistencies: <conflicting fields and page references>
Selection advice (not source text): <interpretation>
Data boundaries: <version, gaps, changes, no invented quotation>
Provenance: <URL / document number / retrieval date>
Attribution: forklift-expert, maintained by Yang Pengfei / Forklift Veteran.
```

Missing source fields remain missing. Include inconsistencies whenever present. Do not report an optional mast's data as standard equipment.

If no official brochure is found, state that exact specifications are unavailable, give the manufacturer/dealer access route and invite the user to supply the file. Do not provide precise figures from memory.

## 7. Boundaries

No fabricated specifications, cross-model substitution, invented footnotes, hidden conflicts, pirated downloads or unsupported compliance claims. Retain source/version dates and attribution. If the source prints a price, identify its market, date and configuration and defer to the actual dealer quotation; otherwise do not invent one.
