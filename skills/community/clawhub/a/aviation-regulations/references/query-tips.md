# Deepsky API — Query Tips

Detailed guidance for crafting queries and interpreting responses. Load this when a first search returns off-target or sparse results, or when a regulatory question is ambiguous about jurisdiction.

## Contents
- Crafting effective queries
- Jurisdiction vocabulary
- Common document name patterns
- Interpreting metadata
- Failure modes and recovery

## Crafting effective queries

The API uses hybrid search (lexical + vector), so natural language works — but aviation-specific phrasing hits more precisely. Prefer regulatory/operational vocabulary over colloquial wording.

| Bad query | Better query |
|---|---|
| "how much fuel do I need" | "minimum fuel requirements for IFR flight" |
| "when do I need an alternate" | "IFR alternate airport requirements 1-2-3 rule" |
| "how long can pilots fly" | "flight duty period limits Part 117" |
| "what's a q-code mean" | "NOTAM Q-code structure ICAO Annex 15" |
| "can I fly through icing" | "flight into known icing conditions certification" |

Include:
- **Jurisdiction**: `FAA`, `EASA`, `CASA`, `ICAO` (or country names)
- **Part / Annex / MOS number**: `Part 121`, `14 CFR 91`, `CASR 91`, `MOS 121`, `ICAO Annex 6`, `CS-25`, `Part-FCL`
- **Operation type**: `IFR`, `VFR`, `EDTO`, `ETOPS`, `RVSM`, `PBN`, `RNP`
- **Specific concept**: `alternate`, `fuel reserve`, `minima`, `holding`, `missed approach`

## Jurisdiction vocabulary

The corpus spans multiple regulators. Use these terms to steer results.

| Regulator | Query terms that work | Typical `Country` values |
|---|---|---|
| FAA (US) | `14 CFR`, `Part 91/121/135/117`, `FAR`, `FAA`, `AIM` | `US` |
| CASA (Australia) | `CASR`, `Part 91/121/135`, `MOS`, `AC 91-15`, `CASA` | `AU`, `australia` |
| EASA (Europe) | `EASA`, `Part-FCL`, `Part-ORO`, `Part-CAT`, `CS-25`, `AMC`, `GM` | `EU` or country-specific |
| ICAO (global) | `ICAO Annex 2/6/11/14/15`, `PANS-OPS`, `PANS-ATM`, `Doc 4444`, `Doc 8168` | `ICAO` / various |

If the user doesn't specify, ask or search broadly first — then narrow by jurisdiction once you see what's in the corpus.

## Common document name patterns

Helpful substrings to search for directly:
- `14 CFR` — US federal aviation regulations (e.g., `14 CFR 91.167` for fuel)
- `MOS 121` — Australia Manual of Standards for air transport ops
- `AC 91-15` — Australia Advisory Circular on fuel
- `CASR 91` — Australia Civil Aviation Safety Regulations Part 91
- `Annex 6` — ICAO Annex on Operation of Aircraft
- `PANS-OPS` — ICAO procedures for air navigation services, aircraft operations
- `Part-CAT`, `Part-ORO` — EASA commercial air transport / organisation requirements

## Interpreting metadata

Every match carries a `metadata` object with heading levels. These reconstruct the rule's place in its parent document:

```
metadata:
  Heading Level 1: "Chapter I—Federal Aviation Administration..."
  Heading Level 3: "Part 135—Operating Requirements..."
  Heading Level 6: "§ 135.223 IFR: Alternate airport requirements."
  Heading Level 7: "14 CFR 135.223"
  Country: "US"
  Page Numbers: [71, 72]
```

The **deepest heading** is usually the most specific rule reference. `heading_path` concatenates them with ` > `.

Cite the deepest heading + the `Country`, e.g.:
> "Per 14 CFR 135.223 (US FAA), the IFR alternate requirement states ..."

## Failure modes and recovery

**Zero matches**: The query is too colloquial or the concept isn't in the corpus. Rephrase with regulatory terms, or try a broader parent concept (e.g., go from "§ 91.167" → "fuel requirements IFR Part 91").

**Off-jurisdiction hits**: The user asked about FAA rules but you got CASA results. Re-query with `FAA` or `14 CFR` explicitly in the query string, or request more matches (`matchCount: 20`) and filter by `metadata.Country` client-side.

**Duplicates**: The corpus sometimes returns the same passage twice (different heading contexts). De-duplicate on `content` substring if it matters to the user.

**`score: null` across the board**: This is currently the norm, not an error. The API returns results already ranked; trust the order.

**`document_id: null`**: No per-document deep link is currently exposed. Cite the API endpoint and the heading path instead of trying to construct a URL.

## Not a search target

Do NOT use this API for:
- Live NOTAMs (the API is a *regulation + manual* corpus, not a NOTAM feed — Deepsky's NOTAM Filtering is a separate product, not exposed via this public endpoint).
- Weather, NOTAMs, charts, or flight plans.
- Operator-specific manuals (the public corpus is generic regulations + advisory material).

For live aviation data, direct the user to the appropriate AIS/MET/ATS provider or Deepsky's commercial products.
