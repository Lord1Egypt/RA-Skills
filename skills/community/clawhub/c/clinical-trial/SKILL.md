---
name: clinical-trial-search
description: "Search clinical trial databases similar to ClinicalTrials.gov. Use this skill whenever the user asks about clinical trials, drug trials, indications, targets, drug names, trial phases, NCT IDs, enrollment, or recruitment. Automatically parses natural language questions into structured query parameters and calls the backend API to return matching trial records. Trigger words include: clinical trial, NCT, drug development, indication, target, phase, enrollment, recruitment, sponsor, cohort, arm, endpoint, efficacy, safety data."
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["NOAH_API_TOKEN"]},"primaryEnv":"NOAH_API_TOKEN" } }
---

# Clinical Trial Search Skill

This skill converts natural language questions into structured API queries against a clinical trial database, then presents the results in a readable format.

## Workflow

1. **Parse user intent** — Extract key entities from the user's question
2. **Build query parameters** — Map entities to the query schema below
3. **Execute the query** — Run `scripts/search.py`
4. **Present results** — Format and display trials to the user

## Step 1: Extract Keywords

Identify the following entity types from the user's question:

| Field | Type | Description                       | Example                                                   |
|-------|------|-----------------------------------|-----------------------------------------------------------|
| `nctid` | `List[str]` | NCT identifier(s)                 | `["NCT04280783"]`                                         |
| `acronym` | `List[str]` | Trial acronym(s)                  | `["KEYNOTE-590"]`                                         |
| `company` | `List[str]` | Sponsor company name(s)           | `["Pfizer", "Roche"]`                                     |
| `indication` | `List[str]` | Disease / indication              | `["lung cancer", "NSCLC"]`                                |
| `phase` | `List[str]` | Trial phase(s)                    | `["Preclinical", "I", "II", "III", "IV", "Others"]`                                  |
| `target` | `dict` | Biological target(s)              | `{"logic": "or", "data": ["PD-1", "VEGF"]}`               |
| `drug_name` | `dict` | Drug name(s)                      | `{"logic": "or", "data": ["pembrolizumab"]}`              |
| `drug_modality` | `dict` | Drug modality  | `{"logic": "or", "data": ["Vaccine", "mRNA"]}` |
| `drug_feature` | `dict` | Drug feature(s) | `{"logic": "or", "data": ["Biologic", "Non-NME"]}`                 |
| `location` | `dict` | Trial location(s)                 | `{"logic": "or", "data": ["China", "United States", "Japan"]}`               |
| `has_result_summary` | `bool` | Only trials with result summaries | `true`                                                    |
| `official_data` | `bool` | Only official data sources        | `false`                                                   |
| `page_num` | `int` | Page index (0-based)              | `0`                                                       |
| `page_size` | `int` | Results per page (1–200)          | `10`                                                       |

**Dict field format:**
```json
{"logic": "or", "data": ["value1", "value2"]}
```

- `logic` controls how multiple values are combined: `"or"` (any match) or `"and"` (all must match). Default to `"or"` unless the user explicitly wants all terms to apply simultaneously.
- `data` is the list of keyword strings to match.

**Type rules:**
- `indication`, `acronym`, `company`, `nctid`, `phase` → plain `List[str]`
- `target`, `drug_name`, `drug_modality`, `drug_feature`, `location`, `route_of_administration` → `dict` with `logic` and `data`
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
- `total_count` — total number of matching trials
- `results` — current page of results, each with NCT ID, title, phase, status, indication, drugs, sponsor, etc.

If results exceed 100, prompt the user to narrow the query. If no results are returned, apply the fallback strategies below before giving up.

## Step 3: Review and Fallback Search Strategies
If no results are returned, apply the fallback strategies below before giving up.
When an initial query returns zero or poor results, try these strategies **in order**:

### Strategy 1 — Drug Name Variant Expansion

Trial registries may store drug names inconsistently (INN vs brand name, with/without hyphens, partial codes). Expand `drug_name.data` to include multiple variants in a single `or` query.

```json
{
  "drug_name": {"logic": "or", "data": ["SHR-A1904", "SHR A1904", "A1904", "SHR1904"]},
  "page_num": 0,
  "page_size": 50
}
```

Also try substituting the trial acronym if known:
```json
{
  "acronym": ["KEYNOTE-590", "KEYNOTE590", "KN590"],
  "page_num": 0,
  "page_size": 10
}
```

**Common variant patterns:**
- Remove or replace hyphens: `SHR-A1904` → `SHR A1904`, `SHRA1904`
- Strip prefix: `9MW-2821` → `MW-2821`, `9MW2821`
- Try both INN and internal code together in the same `data` array

---

### Strategy 2 — Sponsor-First with Application-Layer Filtering

When drug name matching is unreliable, anchor on the sponsor company and pull a broad result set, then filter locally by indication, phase, or modality.

```json
{
  "company": ["Roche", "Roche Inc"],
  "page_num": 0,
  "page_size": 200
}
```

After retrieval, apply local filters:
- `phase in ["II", "III"]`
- `indication contains "breast cancer"`
- `drug_name matches known code pattern`

Use this strategy when the drug code is ambiguous or when searching for a company's full trial portfolio.

---

### Strategy 3 — Broad Target/Indication Search with Post-Filtering

When neither drug name nor company yields results, search by biological target and indication, then narrow client-side by sponsor or drug name pattern.

```json
{
  "target": {"logic": "or", "data": ["CLDN18.2", "Nectin-4", "HER2"]},
  "indication": ["gastric cancer", "breast cancer"],
  "page_num": 0,
  "page_size": 200
}
```

After retrieval, filter by:
- Sponsor name substring (e.g. contains `"Hengrui"`)
- Drug code prefix (e.g. starts with `SHR`, `9MW`, `A166`)
- Trial status (`Recruiting`, `Active, not recruiting`)

> **Note:** If the API supports regex, patterns like `(SHR|9MW|A166)` can be passed directly in `drug_name.data` to broaden matching in a single call.

---

### Strategy 4 — Relax Filters Incrementally

If all strategies above still return no results, drop filters one at a time in this order:

1. Drop `has_result_summary` (many trials have no posted results)
2. Drop `phase` filter
3. Drop `location` filter
4. Broaden `indication` (e.g. `"NSCLC"` → `"lung cancer"` → `"cancer"`)
5. Remove `drug_modality` or `drug_feature` constraints

Re-run after each relaxation and stop as soon as results appear.

---

## Decision Tree

```
Initial query returns results?
├── Yes → present results
└── No  → Strategy 1: expand drug_name / acronym variants
          └── Still no → Strategy 2: sponsor anchor + local filter
                         └── Still no → Strategy 3: target/indication broad search
                                        └── Still no → Strategy 4: relax filters incrementally
Any step hits HTTP 429?
└── Pause entire chain 15s → resume from current strategy
    (sleep ≥5s between every request to avoid triggering 429)
```

---

## Conversion Examples

**User:** "Find Phase 3 trials of PD-1 antibodies in lung cancer that have results"

```json
{
  "target": {"logic": "or", "data": ["PD-1"]},
  "drug_modality": {"logic": "or", "data": ["Monoclonal Antibodies"]},
  "indication": ["lung cancer"],
  "phase": ["III"],
  "has_result_summary": true,
  "page_num": 0,
  "page_size": 10
}
```

---

**User:** "Look up NCT04280783"

```json
{
  "nctid": ["NCT04280783"],
  "page_num": 0,
  "page_size": 1
}
```

---

**User:** "Roche bispecific antibody trials in China"

```json
{
  "company": ["Roche"],
  "location": {"logic": "or", "data": ["China"]},
  "drug_modality": {"logic": "or", "data": ["Bi-specific Antibodies"]},
  "page_num": 0,
  "page_size": 10
}
```

---

**User:** "Oral small molecule KRAS G12C inhibitors in colorectal cancer"

```json
{
  "target": {"logic": "or", "data": ["KRAS G12C"]},
  "drug_modality": {"logic": "or", "data": ["Small Molecule"]},
  "indication": ["colorectal cancer"],
  "page_num": 0,
  "page_size": 10
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