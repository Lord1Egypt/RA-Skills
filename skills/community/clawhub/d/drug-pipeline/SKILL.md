---
name: drug-search
description: "Search a pharmaceutical drug database for pipeline and development information. Use this skill whenever the user asks about drugs by name, target, indication, company, modality, phase, or development progress. Automatically parses natural language questions into structured query parameters and calls the backend API to return matching drug records. Trigger words include: drug, compound, molecule, pipeline, drug target, indication, modality, antibody, small molecule, phase, approved, development stage, sponsor, drug company, bispecific, route of administration."
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["NOAH_API_TOKEN"]},"primaryEnv":"NOAH_API_TOKEN" } }
---

# Drug Pipeline Search Skill

This skill converts natural language questions into structured API queries against a pharmaceutical drug database, then presents the results in a readable format.

## Workflow

1. **Parse user intent** — Extract key entities from the user's question
2. **Build query parameters** — Map entities to the query schema below
3. **Execute the query** — Run `scripts/search.py`
4. **Present results** — Format and display drug records to the user

## Step 1: Extract Keywords

Identify the following entity types from the user's question:

| Field | Type | Description                 | Example                                                   |
|-------|------|-----------------------------|-----------------------------------------------------------|
| `drug_name` | `dict` | Drug name(s)                | `{"logic": "or", "data": ["pembrolizumab"]}`              |
| `company` | `List[str]` | Sponsor / developer company | `["Pfizer", "Roche"]`                                     |
| `indication` | `List[str]` | Disease / indication        | `["lung cancer", "NSCLC"]`                                |
| `target` | `dict` | Biological target(s)        | `{"logic": "or", "data": ["PD-1", "VEGF"]}`               |
| `drug_modality` | `dict` | Drug modality  | `{"logic": "or", "data": ["Vaccine", "mRNA"]}` |
| `drug_feature` | `dict` | Drug feature(s) | `{"logic": "or", "data": ["Biologic", "Non-NME"]}`                 |
| `phase` | `List[str]` | Development phase(s)        | `["Preclinical", "I", "II", "III", "IV", "Others", "IND", "Suspended", "Approved", "Unknow", "Withdraw from Market", "BLA/NDA"]`                                 |
| `route_of_administration` | `dict` | Route of administration (requires exact formatted values) | `{"logic": "or", "data": ["Intravenous (IV)", "Oral (PO)"]}`                 |
| `page_num` | `int` | Page index (0-based)        | `0`                                                       |
| `page_size` | `int` | Results per page (1–2000)      | `200`                                                       |

**Dict field format:**
```json
{"logic": "or", "data": ["value1", "value2"]}
```

- `logic` controls how multiple values are combined: `"or"` (any match) or `"and"` (all must match). Default to `"or"` unless the user explicitly wants all terms to apply simultaneously.
- `data` is the list of keyword strings to match.

**Type rules:**
- `company`, `indication`, `phase`, `location` → plain `List[str]`
- `drug_name`, `target`, `drug_modality`, `drug_feature`, `route_of_administration` → `dict` with `logic` and `data`
- Default to `page_num: 0, page_size: 10` unless the user specifies otherwise
- Prefer English keywords (the database is indexed in English); translate non-English terms
- `drug_modality` must use exact strings from this set:

  ```json
  [
    "Steroids", "Vaccine", "Antisense RNA", "Antibody-Drug Conjugates, ADCs", "Unknown", "Protein Degrader",
    "Monoclonal Antibodies", "mRNA", "Others", "Cell-based Therapies", "Imaging Agents", "Gene Therapy",
    "miRNA", "Polypeptide", "Recombinant Proteins", "Small Molecule", "siRNA/RNAi", "Trispecific Antibodies",
    "Polyclonal Antibodies", "Bi-specific Antibodies", "Glycoconjugates", "Radiopharmaceutical",
    "Nucleic Acid-based", "Carbohydrates"
  ]
  ```
- `drug_feature` must use exact strings from this set:

  ```json
  [
    "505b2", "Bacterial Product", "Biologic", "Biosimilar", "Device", "Fixed-Dose Combination", "Immuno-Oncology",
    "New Molecular Entity (NME)", "Non-NME", "Precision Medicine", "Reformulation", "Specialty Drug", "Viral"
  ]
  ```
- `route_of_administration` must use exact strings from this set:

  ```json
  [
    "Intraarterial", "Intraurethral", "Inhaled", "Intranasal", "Subcutaneous (SQ) - Unspecified", "Transdermal",
    "Intraocular/Subretinal/Subconjunctival", "Subcutaneous (SQ) Injection", "Intrauterine", "Intralymphatic",
    "Intradiscal", "Intra-amniotic", "Intrathecal", "Intracerebral/cerebroventricular", "Intramuscular (IM)",
    "Intraarticular", "Intracochlear", "Surgical Implantation", "Hemoperfusion", "Subcutaneous (SQ) Infusion",
    "Intravitreal", "Intravenous (IV)", "Oral (PO)", "Intradermal", "Percutaneous Catheter/Injection",
    "Intranodal", "Intravesical", "Intracameral", "Intratympanic", "Intratumoral",
    "Sublingual (SL)/Oral Transmucosal", "Intravaginal", "N/A", "Rectal", "Intracavitary",
    "Intra-Cisterna Magna (ICM) Injection", "Injectable - Unspecified", "Intratracheal", "Topical",
    "Instillation", "Intraintestinal", "Submucosal"
  ]
  ```

## Step 2: Execute the Query

```bash
python scripts/search.py --params '<JSON string>'
```

Or using a parameter file:

```bash
python scripts/search.py --params-file /tmp/query.json
```

Add `--raw` to receive the unformatted JSON response.

## Step 3: Interpret Results

The response contains:
- `total_count` — total number of matching drugs
- `results` — current page of drug records, each with name, phase, modality, targets, companies, indication, development progress, etc.

## Step 4: Review and Fallback Search Strategies
If no results are returned, apply the fallback strategies below before giving up.
When an initial query returns zero or poor results, try these strategies **in order**:

### Strategy 1 — Drug Name Variant Expansion

Drug names in the database may use different formats (with/without hyphens, partial codes, aliases). Expand the `drug_name` field to include common variants and merge deduplicated results.

```json
{
  "drug_name": {"logic": "or", "data": ["SHR-A1904", "SHR A1904", "A1904", "SHR1904"]},
  "page_num": 0,
  "page_size": 50
}
```

**Common variant patterns to try:**
- Remove or replace hyphens: `SHR-A1904` → `SHR A1904`, `SHRA1904`
- Strip prefix/suffix: `9MW-2821` → `MW-2821`, `9MW2821`
- Known alias: include trade names or INN alongside internal codes

---

### Strategy 2 — Company-First with Application-Layer Filtering

When drug name matching is unreliable, use the company as the anchor. Fetch a broad set of the company's drugs, then filter by modality/indication/target in post-processing.

```json
{
  "company": ["Roche", "Roche Inc"],
  "page_num": 0,
  "page_size": 500
}
```

After retrieving results, apply local filters:
- `modality == "Monoclonal Antibodies"`
- `indication contains "breast cancer"`
- `drug_name matches known code pattern`

Use this strategy when the drug code is ambiguous or the API match rate is low.

---

### Strategy 3 — Broad Target/Modality Search with Post-Filtering

When neither name nor company is reliable, search by biological target and modality, then narrow results client-side.

```json
{
  "target": {"logic": "or", "data": ["CLDN18.2", "Nectin-4", "HER2"]},
  "drug_modality": {"logic": "or", "data": ["Monoclonal Antibodies"]},
  "page_num": 0,
  "page_size": 200
}
```

After retrieval, filter by company name or drug code pattern using substring matching (e.g. code starts with `SHR`, `9MW`, `A166`).

> **Note:** If the API supports regex, patterns like `(SHR|9MW|A166)` can be passed directly in `drug_name.data` to broaden matching in a single call.

---

## Decision Tree

```
Initial query returns results?
├── Yes → present results
└── No  → Strategy 1: expand drug_name variants
          └── Still no results → Strategy 2: company anchor + local filter
                                 └── Still no results → Strategy 3: target/modality broad search
Any step hits HTTP 429?
└── Pause entire chain 30s → resume from current strategy
    (sleep ≥5s between every request to avoid triggering 429)
```

---

## Conversion Examples

**User:** "Find PD-1 antibodies in Phase 3"

```json
{
  "target": {"logic": "or", "data": ["PD-1"]},
  "drug_modality": {"logic": "or", "data": ["Monoclonal Antibodies"]},
  "phase": ["III"],
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Roche bispecific antibodies for lung cancer"

```json
{
  "company": ["Roche"],
  "drug_modality": {"logic": "or", "data": ["Bi-specific Antibodies"]},
  "indication": ["lung cancer"],
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Oral small molecule KRAS G12C inhibitors"

```json
{
  "target": {"logic": "or", "data": ["KRAS"]},
  "drug_modality": {"logic": "or", "data": ["Small Molecule"]},
  "route_of_administration": {"logic": "or", "data": ["Oral (PO)"]},
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Drugs targeting both PD-1 and VEGF"

```json
{
  "target": {"logic": "and", "data": ["PD-1", "VEGF"]},
  "page_num": 0,
  "page_size": 30
}
```

---

**User:** "Look up pembrolizumab"

```json
{
  "drug_name": {"logic": "or", "data": ["pembrolizumab"]},
  "page_num": 0,
  "page_size": 30
}
```

---

## Dependencies

- Python 3.8+
- `requests` library (`pip install requests`)
- Environment variable `NOAH_API_TOKEN` — API authentication token (required)
  - Register for a free account at [noah.bio](https://noah.bio) to obtain your API key.

---

## Security & Packaging Notes

- This skill only calls NoahAI official HTTPS endpoints under `https://www.noah.bio/api/` and does not contact third-party services.
- It requires exactly one environment variable: `NOAH_API_TOKEN`. Store it in the environment or a local `.env` file, and never place it inline in commands, chats, or packaged files.
- The token is scoped to read medical public details only and cannot access private user records.
- The skill does not intentionally persist request parameters locally. Any server-side retention is determined by the NoahAI API service and its operational logging policies.
- It does not request persistent or system-level privileges and does not modify system configuration.
- The skill is source-file based (Python scripts only) and does not require runtime installs, package downloads, or external bootstrap steps.