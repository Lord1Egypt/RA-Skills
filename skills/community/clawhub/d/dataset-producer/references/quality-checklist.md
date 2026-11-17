# Quality Checklist — Run Before Declaring the Dataset Done

> A publishable dataset passes every check on this list. Run through it sequentially; fix anything that fails. If a check is genuinely N/A, note why in the README rather than skipping silently.
>
> The checklist is organized in seven sections matching the production pipeline stages.

## Table of Contents

- [1. Repository structure](#1-repository-structure)
- [2. YAML frontmatter](#2-yaml-frontmatter)
- [3. README body](#3-readme-body)
- [4. Datasheet coverage (Datasheets for Datasets)](#4-datasheet-coverage-datasheets-for-datasets)
- [5. Technical / data-quality checks](#5-technical--data-quality-checks)
- [6. Licensing and attribution](#6-licensing-and-attribution)
- [7. Reproducibility and discovery](#7-reproducibility-and-discovery)

---

## 1. Repository structure

- [ ] `README.md` exists at the repo root.
- [ ] `LICENSE` (or `LICENSE.md` / `LICENSE.txt`) exists at the repo root and contains the full license text matching the YAML `license:` field.
- [ ] `data/` directory exists (or `data/<config>/` for multi-config).
- [ ] Parquet files use the naming convention: `<split>-<NNNNN>-of-<NNNNN>.parquet`.
- [ ] Shard count and indices are zero-padded to 5 digits (`00000-of-00003`, not `0-of-3`).
- [ ] No "scratch" files in the repo (`.DS_Store`, `__pycache__/`, `*.bak`, editor swap files).
- [ ] `create_dataset.py` (or equivalent provenance script) committed alongside the data.
- [ ] `.gitattributes` declares parquet/jsonl as LFS-tracked (HF auto-generates this on first push; for local datasets, skip).

### Example correct structure

```
my_dataset/
├── README.md
├── LICENSE
├── create_dataset.py
└── data/
    ├── train-00000-of-00003.parquet
    ├── train-00001-of-00003.parquet
    ├── train-00002-of-00003.parquet
    ├── test-00000-of-00001.parquet
    └── validation-00000-of-00001.parquet
```

---

## 2. YAML frontmatter

- [ ] YAML block delimited by `---` on its own line at the very start of `README.md` (no leading blank lines, no BOM).
- [ ] `license:` field present and matches an SPDX identifier (e.g., `cc-by-4.0`, `apache-2.0`, `mit`).
- [ ] `language:` field is a list of ISO 639-1 codes (`en`, `hi`, `zh`, …).
- [ ] `pretty_name:` present (human-readable name; this is what shows in the Hub UI).
- [ ] `size_categories:` is a single string (NOT a list), and the bucket matches the total row count across all splits.
- [ ] `task_categories:` is a list of valid top-level ML tasks (see `yaml-spec.md` taxonomy).
- [ ] `configs:` block present, even for single-config datasets (`config_name: default` is required).
- [ ] Each `configs` entry has `data_files:` with explicit `split:` and `path:` mappings.
- [ ] `default: true` set on one config if there are multiple.
- [ ] `dataset_info:` block present and declares `features:` and `splits:` explicitly.
- [ ] Each `splits:` entry has `num_bytes:` and `num_examples:` (not just `num_examples:`).
- [ ] `download_size:` and `dataset_size:` present and accurate (computed from actual files, not estimated).
- [ ] All `dtype:` values are valid types from the type vocabulary (see `yaml-spec.md`).
- [ ] `ClassLabel` fields declare `names:` mapping int → string label.
- [ ] `viewer:` is set to `false` only if the dataset is too large for the Viewer (> 100 GB); otherwise omitted (defaults to `true`).

### Verification

Run the `datasets` library's YAML validator:

```bash
python -c "from datasets import load_dataset; ds = load_dataset('path/to/dataset'); print(ds)"
```

If it loads and the splits match what you declared, the YAML is correct.

---

## 3. README body

- [ ] `# Dataset Card for <Name>` heading at the top (after YAML).
- [ ] `## Dataset Description` section with the 5-bullet list (Homepage, Repository, Paper, Leaderboard, Point of Contact).
- [ ] `### Dataset Summary` — 1–3 paragraphs covering what / how many / why.
- [ ] `### Supported Tasks and Leaderboards` — list of ML tasks the dataset supports.
- [ ] `### Languages` — BCP-47 codes + plain-language description.
- [ ] `## Dataset Structure` section.
- [ ] `### Data Instances` — a fenced ```json block with one concrete example row.
- [ ] `### Data Fields` — bullet list of every column: name, type, meaning.
- [ ] `### Data Splits` — markdown table of split → row counts.
- [ ] `## Dataset Creation` section.
- [ ] `### Curation Rationale` — why the dataset was built.
- [ ] `### Source Data` — where the raw data came from + cleaning applied.
- [ ] `### Annotations` — how labels/scores were produced + who annotated.
- [ ] `### Personal and Sensitive Information` — PII scan results, removal process.
- [ ] `## Considerations for Using the Data` — social impact, biases, limitations.
- [ ] `## Additional Information` section.
- [ ] `### Dataset Curators` — people/orgs responsible.
- [ ] `### Licensing Information` — SPDX code + link to LICENSE file.
- [ ] `### Citation Information` — BibTeX block in a ```bibtex fence.
- [ ] `### Contributions` — GitHub handles of contributors.

### Quality checks

- [ ] No `[More Information Needed]` placeholders in sections you can fill (it's a last-resort marker, not a default).
- [ ] Every URL in the README resolves (no 404s on Homepage/Repository/Paper links).
- [ ] The example row in `### Data Instances` matches the actual schema (validate by `python -c "from datasets import load_dataset; print(load_dataset('path')['train'][0])"`).
- [ ] The Data Fields list matches the YAML `features:` block (same field names, same order, same types).
- [ ] No artificial ending markers like "------End of Report------" or "======Document Ends======".
- [ ] Citation BibTeX parses cleanly (test with `bibtex` or a validator).

---

## 4. Datasheet coverage (Datasheets for Datasets)

The [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) framework (Gebru et al., 2021) defines 7 sections that every dataset should document. Cross-check that your README answers the key questions from each:

### Motivation
- [ ] For what purpose was the dataset created? (in `### Curation Rationale`)
- [ ] Who created the dataset? (in `### Dataset Curators`)
- [ ] Who funded the creation? (often in `### Curation Rationale`)

### Composition
- [ ] What do the instances represent? (in `### Dataset Summary`)
- [ ] How many instances are there? (in `### Data Splits`)
- [ ] Does the dataset contain all possible instances, or is it a sample? (in `### Curation Rationale`)
- [ ] Are there recommended data splits? (in `### Data Splits`)
- [ ] Are there any errors / sources of noise / known limitations? (in `### Other Known Limitations`)

### Collection process
- [ ] How was the data collected? (in `### Source Data → Initial Data Collection and Normalization`)
- [ ] What strategies were used to ensure diversity? (in `### Curation Rationale`)
- [ ] Over what timeframe was the data collected? (in `### Source Data`)

### Preprocessing / cleaning / labeling
- [ ] What preprocessing/cleaning was done? (in `### Source Data`)
- [ ] Was the "raw" data saved in addition to the preprocessed/cleaned data? (mention `raw/` directory if applicable)
- [ ] Is the labeling software open-source? (in `### Annotations`)

### Uses
- [ ] What are the intended uses? (in `### Dataset Summary`)
- [ ] What are the out-of-scope uses? (often added as a `### Out-of-Scope Use` subsection — BharatGen's READMEs miss this; don't follow that example)
- [ ] What tasks could the dataset be used for? (in `### Supported Tasks and Leaderboards`)

### Distribution
- [ ] How will the dataset be distributed? (HF Hub, AIKosh, etc. — usually implicit)
- [ ] When will the dataset be distributed? (often implicit; add a release date)
- [ ] Under what license? (in `### Licensing Information`)
- [ ] Are there any copyrights or IP restrictions? (in `### Licensing Information`)

### Maintenance
- [ ] Who maintains the dataset? (in `### Dataset Curators`)
- [ ] How can the maintainer be contacted? (in `### Dataset Description → Point of Contact`)
- [ ] Is there an erratum? (optional but valuable — BharatGen misses this)
- [ ] Will the dataset be updated? (often in `### Curation Rationale` or a `## Versions` section)

---

## 5. Technical / data-quality checks

Run these via `scripts/validate.py`:

### Schema conformance
- [ ] Every row matches the declared `Features`. Mismatched types or missing fields raise `ArrowInvalid` early.
- [ ] No silent type coercion (e.g., `int64` column with a `null` value silently becoming `float64`).
- [ ] `ClassLabel` columns contain only valid integer indices (0 to `len(names) - 1`).

### Deduplication
- [ ] Exact dedup on a canonical JSON hash of each row. Report dedup rate in the README.
- [ ] For pretraining corpora: fuzzy dedup (MinHash LSH) also run.
- [ ] For benchmarks: check no question appears in both `train` and `test`.

### PII scan
- [ ] Regex scan for emails, phone numbers (US + international), SSNs, credit-card numbers.
- [ ] Optional: `presidio` for higher-precision PII detection.
- [ ] Flag rows with PII; don't auto-redact unless the user explicitly asked.
- [ ] If PII was found and redacted, document the redaction in `### Personal and Sensitive Information`.

### Contamination check
- [ ] If the dataset is for training: scan for known benchmark prompts (MMLU, GSM8K, HumanEval) that leaked in.
- [ ] Add a boolean `in_<bench>_train` column for each contaminated benchmark (UltraFeedback Binarized does this for GSM8K).
- [ ] Report contamination rate in `### Other Known Limitations`.

### Length distribution
- [ ] Compute min / p25 / median / p75 / max length for the main text fields.
- [ ] Flag outliers (empty strings, 100K-char walls of text).
- [ ] Document length distribution in `### Other Known Limitations` if extreme.

### Language ID (for multilingual datasets)
- [ ] Run fastText LID; store `language` + `language_score` per row.
- [ ] Flag rows below 0.7 confidence for manual review.
- [ ] Report per-language row counts in `### Data Splits` or a `## Summary Statistics` section.

### ClassLabel balance (for benchmarks)
- [ ] For MCQ: check the answer distribution is roughly uniform across A/B/C/D. Imbalance suggests annotation bias.
- [ ] For classification: report class distribution; flag if max-class / min-class > 10×.

### Token count (for pretraining corpora)
- [ ] Run a tokenizer over the main text column; store `token_count` per row.
- [ ] Report total token count in `### Dataset Summary`.
- [ ] Compute per-shard token counts for sampling budgets.

### Row size (for the Viewer)
- [ ] No row exceeds 2 MB (`viewer_row_size_mb`). Large image/audio/embedding columns may push past this — consider WebDataset instead.

---

## 6. Licensing and attribution

- [ ] The `license:` YAML field matches the actual license of the **source data** (not just what you'd like it to be).
- [ ] If the source is multi-licensed, use a list: `license: [cc-by-4.0, mit]`.
- [ ] If the source is non-commercial (e.g., Alpaca's underlying text-davinci-003 outputs), use `cc-by-nc-4.0` or `other` with an explanation.
- [ ] If the source has a custom license, use `license: other` and add a sentence in `### Licensing Information` explaining.
- [ ] The `LICENSE` file in the repo root contains the full license text (not just a SPDX identifier).
- [ ] If the dataset was derived from another dataset, cite the upstream in `### Citation Information` (add a second BibTeX block if needed).
- [ ] If the dataset contains LLM-generated content, the OpenAI / Anthropic / etc. terms of service may restrict redistribution. Document this in `### Licensing Information`.

### Common license pitfalls

- **Scraping copyrighted websites and re-licensing as `cc-by-4.0`** — you can't grant rights you don't have. Use `other` with an explanation.
- **Using text-davinci-003 outputs and re-licensing as `mit`** — OpenAI's terms require attribution and prohibit using outputs to train competing models. Use `cc-by-nc-4.0` (Alpaca's choice) or `other`.
- **Mixing Wikipedia (CC-BY-SA) with closed-source data** — the resulting dataset is `cc-by-sa-4.0` for the Wikipedia parts and `other` for the rest. List both: `license: [cc-by-sa-4.0, other]`.

---

## 7. Reproducibility and discovery

### Reproducibility
- [ ] `create_dataset.py` (or equivalent) committed and runnable from scratch.
- [ ] The script reads from publicly-available sources (URLs, public datasets, bundled raw files). If it requires private API keys or local files, document that.
- [ ] Random seeds set explicitly (e.g., `random.seed(42)`, `np.random.seed(42)`) for sampling/shuffling.
- [ ] Filter stats recorded (how many rows were dropped at each filter step). FineWeb publishes these in `## Summary Statistics`.
- [ ] Software versions pinned (optional but valuable for reproducibility — add a `requirements.txt` or document in the README).
- [ ] Git tag or HF revision pin for the released version (`v1.0`, `v1.1`, …) so `load_dataset(..., revision="v1.0")` is reproducible.

### Discovery (Hub-specific)
- [ ] Tags include the modality (`text`, `image`, `audio`, `video`, `tabular`, `timeseries`, `geospatial`, `3d`).
- [ ] Tags include any associated library (`datasets`, `argilla`, `distilabel`, `pandas`, `mlcroissant`, `webdataset`).
- [ ] `paperswithcode_id:` set if the dataset has a PapersWithCode page.
- [ ] `arxiv:<id>` tag auto-injected when an arXiv link is present in the README.
- [ ] Description (in the README `### Dataset Summary`) is informative enough to find via search.
- [ ] The dataset is in the right Hub namespace (org for institutional, personal for individual).
- [ ] The dataset is set to public (not private) when ready to publish.

---

## Final smoke test

After everything passes, do an end-to-end smoke test:

```python
from datasets import load_dataset

# 1. Load it
ds = load_dataset("/path/to/my_dataset")

# 2. Verify splits
print(ds)                    # should show all splits with correct row counts

# 3. Verify schema
print(ds["train"].features)  # should match the YAML features block

# 4. Verify a row matches the example in the card
print(ds["train"][0])

# 5. Verify ClassLabel (if applicable)
print(ds["train"].features["answer"].names)   # ['A', 'B', 'C', 'D']
print(ds["train"][0]["answer"])                # int
print(ds["train"].features["answer"].int2str(ds["train"][0]["answer"]))   # 'C'
```

If all five checks pass, the dataset is publish-ready.

---

## Common failures (and how to fix them)

| Failure | Cause | Fix |
|---|---|---|
| `load_dataset` fails with "no splits found" | File names don't match `<split>-XXXXX-of-XXXXX.parquet` pattern, and no YAML `configs.data_files` declared | Rename files OR add explicit `data_files:` mapping in YAML |
| Dataset Viewer shows "no supported files" | Parquet files are in the wrong directory (e.g., `dataset/` instead of `data/`) | Move to `data/` OR point `data_files:` at the actual path |
| Viewer renders `answer` as int, not dropdown | `answer` declared as `dtype: int64` instead of `class_label:` | Change to `dtype: class_label: names: ...` in YAML |
| Size badge shows "unknown" | `size_categories:` missing or wrong format | Add `size_categories: <bucket>` (single string, not a list) |
| License badge missing | `license:` field missing or wrong SPDX key | Add `license: <spdx-id>` matching the SPDX table in `yaml-spec.md` |
| Task filter doesn't show the dataset | `task_categories:` missing or invalid value | Add `task_categories: [<task>]` with a valid top-level task |
| `load_dataset` returns 0 rows | Glob pattern matches no files | Verify file paths in `data_files:` are correct |
| Citation BibTeX doesn't render | Missing ```bibtex fence around the BibTeX block | Wrap BibTeX in ```bibtex ... ``` |
| Auto-conversion still running after upload | You uploaded CSV/JSON instead of parquet | Upload native parquet to skip the conversion queue |
