---
name: dataset-producer
description: Produce complete, publish-ready AI/ML datasets in HuggingFace format (parquet shards + README.md with YAML frontmatter + dataset card + provenance script). Use whenever the user wants to create, build, produce, assemble, package, or publish a dataset for training, fine-tuning, evaluation, or benchmarking — including instruction-tuning (SFT), chat/dialogue, preference/DPO/RLHF, pretraining corpora, MCQ benchmarks, QA datasets, or any structured data meant to be loaded by `datasets.load_dataset()` or pushed to HF. Trigger on phrases like "make a dataset from these documents", "build a benchmark", "package this for fine-tuning", "convert this JSONL to a HuggingFace dataset", "produce a DPO/preference/SFT dataset", "I want to publish a dataset". Handles schema design, validation, parquet sharding, statistics, card generation, and provenance — the full production pipeline. Prefer this over hand-rolling dataset code whenever the deliverable is a dataset the user will load, share, or train on.
license: MIT
---

# Dataset Producer Skill

Produce complete, publish-ready datasets in the canonical HuggingFace format used by top datasets like MMLU, GSM8K, UltraChat 200k, UltraFeedback Binarized, Alpaca, OASST, FineWeb, Dolma, and BharatGen's BhashaBench family.

This skill ships with a **production pipeline** that has been hardened against the small-data edge cases that bite first-time dataset producers: empty splits, broken ClassLabel YAML, `dataset_size < download_size`, multi-PII-per-field detection, and `make_card.py` crashing on `Sequence of scalars`. Use the bundled scripts rather than reinventing them.

A "complete dataset" here means **all four artifacts**, every time:

1. **Parquet data files** — sharded as `<split>-<NNNNN>-of-<NNNNN>.parquet` under `data/`
2. **`README.md`** — YAML frontmatter (`license`, `language`, `task_categories`, `configs`, `dataset_info`, `size_categories`, `pretty_name`) + canonical dataset-card sections
3. **`create_dataset.py`** — provenance script that reproduces the parquet from raw inputs
4. **`LICENSE`** + **citation block** in the README — so the dataset is legally usable and citable

Skipping any of these makes the dataset harder to load, harder to trust, and harder to cite. We don't skip.

## When to use this skill

Trigger whenever the user wants to **produce, build, assemble, package, or publish** a dataset. Common phrasings:

- "Make a dataset from these PDFs / web pages / CSV files / API responses"
- "Build a benchmark for X"
- "Package this data for fine-tuning / SFT / DPO / pretraining"
- "Convert this JSONL / CSV / JSON into a HuggingFace dataset"
- "I want to publish a dataset to HuggingFace"
- "Produce a preference / DPO / RLHF dataset"
- "Assemble an instruction-tuning dataset"
- "Make a multiple-choice / QA / chat dataset"

If the user is just *analyzing* an existing dataset (counting rows, plotting distributions), do NOT use this skill — that's a data-analysis task. This skill is for **producing** new datasets.

## The seven-stage production pipeline

Every dataset goes through these stages. Skipping a stage produces a worse dataset; the order matters.

```
1. INTENT     →  What kind of dataset? What's the source?
2. SCHEMA     →  Pick the feature family (instruction / chat / preference / pretraining / benchmark / custom)
3. COLLECT    →  Gather raw rows (web-reader, file reads, generators, API, transform existing data)
4. VALIDATE   →  Schema conformance, dedup, PII scan, contamination check, quality filters
5. CONVERT    →  Build parquet shards with proper naming
6. STATISTICS →  num_examples, num_bytes, download_size, size_categories, token_count
7. PACKAGE    →  README.md (YAML + card), LICENSE, create_dataset.py, save to disk or push to Hub
```

Detailed playbook for each stage is below.

### Stage 1 — INTENT

Before writing any code, answer these questions in your head and confirm with the user if anything is unclear:

- **Family**: instruction-tuning (SFT) · chat/dialogue · preference/DPO/RLHF · pretraining corpus · benchmark (MCQ/QA) · generic tabular
- **Source**: existing files (which?) · URLs to scrape · another dataset to transform · LLM-generated · crowd-sourced · hand-written
- **Splits**: train only · train+test · train+val+test · custom (e.g. `train_sft`, `train_prefs`)
- **Languages**: ISO 639-1 codes (`en`, `hi`, `zh`, …)
- **License**: who owns the source data, and what can the user legally re-license it as? Default recommendations: `cc-by-4.0` (permissive, attribution), `apache-2.0` (code-friendly), `mit` (max permissive), `cc-by-nc-4.0` (non-commercial). Use `other` if the source license is unclear and add a sentence in the card explaining.
- **Size target**: a few hundred rows (hand-curated) · 1K-100K (typical SFT) · 100K-1M (large SFT) · 1M+ (pretraining-scale)
- **Output location**: `/home/z/my-project/download/<dataset_name>/` (default) · push to HF Hub (need user's HF token + namespace)

If the user is vague ("make a dataset for me"), ask 2-3 focused questions before proceeding — see `references/clarifying-questions.md`.

### Stage 2 — SCHEMA

Pick the feature family. The five canonical schemas are fully specified in `references/schemas.md` — read that file before writing the schema. Quick reference:

| Family | Core fields | When |
|---|---|---|
| **instruction-tuning** (Alpaca-style) | `instruction`, `input`, `output`, optional `system`, `id`, `source` | Single-turn task → response |
| **chat** (UltraChat-style) | `messages: [{role, content}]`, optional `prompt`, `prompt_id` | Multi-turn dialogue |
| **preference/DPO** (UltraFeedback-style) | `prompt`, `chosen: [{role, content}]`, `rejected: [{role, content}]`, optional `messages`, `score_chosen`, `score_rejected` | RLHF/DPO/ORPO/KTO training |
| **pretraining** (FineWeb-style) | `text`, `id`, `url`, `date`, `source`, `language`, `language_score`, `token_count` | Base-model pretraining |
| **benchmark MCQ** (MMLU-style) | `question`, `subject`, `choices: [string]`, `answer: ClassLabel` | Multiple-choice evaluation |
| **benchmark QA** (SQuAD-style) | `question`, `context`, `answers: {text: [string], answer_start: [int]}` | Extractive QA |

Express the schema as a Python `datasets.Features` object **and** a YAML `dataset_info.features` block — they must match exactly. The Python object is used for validation at build time; the YAML block is what the HuggingFace loader and Dataset Viewer read.

If the user's data doesn't fit any canonical family, design a custom schema following the type vocabulary in `references/yaml-spec.md` (use `Value`, `Sequence`, `list` of structs, `struct`, `class_label`).

### Stage 3 — COLLECT

Gather the raw rows. Common patterns:

- **From local files** (CSV/JSON/JSONL/TXT/PDF): use `pandas`, `json`, `csv`, or `pypdf` to parse, then build a Python list of dicts.
- **From the web** (URLs to scrape): use the **web-reader** skill (`Skill(command="web-reader")`) — `z-ai function -n page_reader -a '{"url": "..."}'` for static pages, or `agent-browser` for JS-rendered ones. Always include the source URL in the row's metadata (the FineWeb schema's `url` field exists for exactly this reason).
- **From another HF dataset**: `from datasets import load_dataset; ds = load_dataset("source/repo")` then transform.
- **LLM-generated**: use the **LLM** skill to generate instructions/responses; record the model name and generation params in a sidecar metadata file.
- **Hand-curated**: write the rows directly in a Python list and validate.

For every row, capture provenance metadata where possible:
- `id` — stable unique ID (UUID or hash of content) for deduplication and tracing
- `source` — where this row came from (URL, file path, generator name)
- `date` — when the source was created or fetched

### Stage 4 — VALIDATE

Run validation **before** converting to parquet — fixing schema issues after sharding is painful. Use `scripts/validate.py` for an automated pass:

```bash
python /home/z/my-project/skills/dataset-producer/scripts/validate.py \
  --input raw.jsonl \
  --features features.json \
  --check schema,dedup,pii,length

# Include contextual PII patterns (IPv4, ISO dates, US ZIP — off by default
# because they have a high false-positive rate in normal text):
python .../validate.py --input ... --features ... --pii-contextual

# Make any PII/contamination finding non-zero-exit (for CI):
python .../validate.py --input ... --features ... --strict
```

The validation suite checks:

1. **Schema conformance** — every row matches the declared `Features`. Mismatched types or missing fields raise `ArrowInvalid` early. CSV/TSV inputs are type-coerced to the declared dtypes first (every CSV cell arrives as a string — without coercion, every numeric column would falsely fail). JSON/JSONL values are used as-is so real type errors in structured data still surface.
2. **Deduplication** — exact-dedup on a canonical JSON hash of each row; optional fuzzy dedup (MinHash LSH) for pretraining corpora. Report the dedup rate.
3. **PII scan** — regex for emails, phone numbers (US + international), SSNs, credit-card numbers. **All PII types in a single field are reported** (the scan does not stop after the first match — a field with both an email and an SSN will report both). Credit-card matches are **Luhn-validated** before reporting, so long digit runs that are really order IDs / serials don't false-positive. Contextual patterns (IPv4, ISO dates, US ZIP) are opt-in via `--pii-contextual` because they have a high false-positive rate in normal text. Use `presidio` for higher-precision PII detection. Flag rows for review; don't auto-redact unless the user asked.
4. **Contamination check** — if the dataset will be used for training, scan for known benchmark prompts (MMLU, GSM8K, HumanEval) that leaked in. Add a boolean `in_<bench>_train` column for each contaminated benchmark.
5. **Length distribution** — compute min/p25/median/p75/max length for the main text fields using **linear interpolation** for percentiles (matches `numpy.percentile` default). Flag outliers (e.g., empty strings, 100K-char walls of text).
6. **Language ID** — for multilingual datasets, run fastText LID and store the `language` + `language_score` per row; flag rows below 0.7 confidence.
7. **ClassLabel balance** — for benchmarks, check that the answer distribution is roughly uniform (MCQ) or report the imbalance.

Print a summary report. If any check fails critically (e.g., 30% PII rate), stop and ask the user before continuing.

### Stage 5 — CONVERT

Build the parquet files. Use the bundled `scripts/produce_dataset.py` — it handles sharding, naming, and split layout automatically:

```bash
python /home/z/my-project/skills/dataset-producer/scripts/produce_dataset.py \
  --input raw.jsonl \
  --features features.json \
  --splits train:0.9,test:0.1 \
  --out /home/z/my-project/download/my_dataset/data/ \
  --shard-size 500MB

# Suppress tqdm progress bars and per-shard log lines (for CI):
python .../produce_dataset.py ... --quiet

# Temporal split (preserve order; first N% → first split — for time-series):
python .../produce_dataset.py ... --split-mode temporal

# Stratified split (balance ClassLabel values across splits — for benchmarks):
python .../produce_dataset.py ... --split-mode stratified --stratify-field answer
# If --stratify-field is omitted, the first ClassLabel in the schema is auto-detected.

# Drop exact duplicates at build time (validate.py reports the rate; this drops them):
python .../produce_dataset.py ... --drop-duplicates

# Add a heuristic token estimate per split to stats.json (chars/4 — sampling budgets only;
# use a real tokenizer for exact counts):
python .../produce_dataset.py ... --token-estimate
```

This produces:

```
my_dataset/
└── data/
    ├── train-00000-of-00003.parquet
    ├── train-00001-of-00003.parquet
    ├── train-00002-of-00003.parquet
    └── test-00000-of-00001.parquet
```

**Empty splits still produce a parquet shard** (with 0 rows) so the README's `data/<split>-*.parquet` glob always matches a file — `load_dataset()` won't break on a 90/10 split where the test split ends up empty.

**`dataset_size` is the in-memory Arrow byte count** (not the JSON-serialized byte count), so the YAML invariant `dataset_size` reflects what `load_dataset()` actually materializes. For very small datasets where parquet metadata overhead dominates, `dataset_size` may be less than `download_size` — that's a known small-data quirk and not a bug.

**Naming convention** (mandatory — the HF loader recognizes this pattern):
```
<split>-<NNNNN>-of-<NNNNN>.parquet
```
- `<split>`: `train`, `test`, `validation`, or custom (`train_sft`, `train_prefs`)
- `<NNNNN>-of-<NNNNN>`: zero-padded shard index and total count, 5 digits each
- Optionally append `-<16-hex-hash>` for content addressing (auto-added by `push_to_hub`)

**Shard size guidance**:
- 1–5 GB per shard for medium datasets (HF's default is 500 MB)
- < 50 GB per file (hard LFS limit is 200 GB)
- < 10,000 files per folder (Git performance threshold)
- For petabyte-scale, use the Dolma URL-manifest pattern instead of hosting files inline

**Media datasets (Image/Audio)**: JSONL can't transport raw bytes, so don't pipe image rows through `--input`. Build them via the library API with real bytes objects in the row dicts: `produce_dataset(rows=[{"image": {"bytes": <png bytes>, "path": None}, "caption": "..."}], features=..., ...)`. The feature parser and YAML generator handle `Image`/`Audio`/`Video` specs (rendered as `dtype: image` / `dtype: audio`), and the shard-size estimator is bytes-safe. For > 10K media files, prefer WebDataset (see `references/format-guide.md`).

**Multi-config datasets** (one directory per config): only when the user genuinely needs multiple schemas or subsets (e.g., MMLU's per-subject configs, FineWeb's per-crawl configs). Don't add a config layer unless it carries real meaning. See `references/multi-config.md`.

### Stage 6 — STATISTICS

After sharding, compute the stats the YAML needs. Use `scripts/produce_dataset.py --stats` (the script does this automatically; the flag is for re-runs):

For each split:
- `num_examples` — row count
- `num_bytes` — decoded Arrow bytes
- `download_size` — on-disk compressed bytes (sum of parquet file sizes)
- `dataset_size` — same as `num_bytes` aggregated across splits

Plus optional aggregate stats to put in the README body:
- Token count (run a tokenizer over the main text column; store per-row as `token_count` for pretraining corpora)
- Per-column null counts
- ClassLabel histograms (for benchmarks)

Map `num_examples` to a `size_categories` bucket (see `references/yaml-spec.md`):
- `n<1K`, `1K<n<10K`, `10K<n<100K`, `100K<n<1M`, `1M<n<10M`, `10M<n<100M`, `100M<n<1B`, `1B<n<10B`, `10B<n<100B`, `100B<n<1T`, `n>1T`

### Stage 7 — PACKAGE

Assemble the four artifacts:

#### 7a. README.md (YAML frontmatter + dataset card)

Generate with `scripts/make_card.py`:

```bash
python /home/z/my-project/skills/dataset-producer/scripts/make_card.py \
  --name "My Dataset" \
  --license "cc-by-4.0" \
  --language en \
  --task text-generation \
  --features features.json \
  --stats stats.json \
  --example example_row.json \
  --out /home/z/my-project/download/my_dataset/README.md

# Skip the manual example_row.json — auto-extract the first row from a parquet shard:
python .../make_card.py ... --auto-example

# If --namespace is omitted, the citation block won't include a Hub URL
# (useful for local-only datasets that won't be pushed to HF).
```

**The YAML generator renders `ClassLabel`, `Sequence` of scalars, `Sequence` of structs, and nested `struct` correctly** — all four forms appear in the canonical schemas (MCQ uses `ClassLabel`, chat uses `Sequence of struct`, QA uses `struct`, instruction-tuning uses `Sequence of string`). The generator builds YAML as direct string output (rather than via `yaml.dump`) so the indentation is exactly what the HF loader expects.

The README must have:

1. **YAML frontmatter** — at minimum `license`, `language`, `task_categories`, `size_categories`, `pretty_name`, `configs`, `dataset_info`. See `references/yaml-spec.md` for the full spec.
2. **Markdown body** — the canonical dataset-card sections:
   - `# Dataset Card for <Name>`
   - `## Dataset Description` (with `Homepage`, `Repository`, `Paper`, `Point of Contact`)
   - `### Dataset Summary` (1–3 paragraphs)
   - `### Supported Tasks and Leaderboards`
   - `### Languages`
   - `## Dataset Structure` (`### Data Instances` with one concrete JSON example, `### Data Fields`, `### Data Splits`)
   - `## Dataset Creation` (`### Curation Rationale`, `### Source Data`, `### Annotations`, `### Personal and Sensitive Information`)
   - `## Considerations for Using the Data` (social impact, biases, limitations)
   - `## Additional Information` (curators, licensing, **citation BibTeX**, contributions)

See `references/card-template.md` for a copy-paste template. Fill every section — use `[More Information Needed]` only as a last resort for fields you genuinely can't fill.

#### 7b. LICENSE file

Copy the matching license text from `assets/licenses/<spdx-id>.txt` into the dataset root. If the user's license isn't bundled, fetch from https://spdx.org/licenses/ or write a minimal one.

#### 7c. create_dataset.py (provenance script)

Save a copy of the build script that produces the parquet from the raw inputs. This is what UltraFeedback Binarized and Argilla's DPO pairs do — committing `create_dataset.py` alongside the data makes the dataset reproducible. The script should:
- Read raw inputs (URLs, files, generator)
- Apply all transforms and filters
- Build the parquet shards
- Print the same statistics that ended up in the YAML

Use `scripts/produce_dataset.py` as the starting point — copy it into the dataset directory and adapt.

#### 7d. Save or push

Default: save everything to `/home/z/my-project/download/<dataset_name>/`. Verify the layout:

```
my_dataset/
├── README.md
├── LICENSE
├── create_dataset.py
└── data/
    ├── train-00000-of-00003.parquet
    ├── train-00001-of-00003.parquet
    ├── train-00002-of-00003.parquet
    └── test-00000-of-00001.parquet
```

Optional: push to the HuggingFace Hub with `huggingface_hub`:

```python
from huggingface_hub import HfApi
api = HfApi(token="hf_...")
api.create_repo(repo_id="username/my-dataset", repo_type="dataset", private=False)
api.upload_folder(folder_path="/home/z/my-project/download/my_dataset",
                  repo_id="username/my-dataset", repo_type="dataset")
```

Only push if the user explicitly asks and provides their HF token — never auto-push.

## Reference files

Read these before writing code:

- **`references/schemas.md`** — Feature schemas (Python `Features` + YAML `dataset_info`) for the five canonical families. **Read this before writing any schema.**
- **`references/yaml-spec.md`** — Complete YAML frontmatter spec: every field, the type vocabulary (`Value`/`Sequence`/`struct`/`list`/`class_label`/`Image`/`Audio`), `configs`/`splits` structure, license identifiers, task_categories/task_ids taxonomy, size_categories buckets.
- **`references/card-template.md`** — Copy-paste README.md template with every section explained.
- **`references/format-guide.md`** — When to use parquet vs JSONL vs CSV vs WebDataset vs URL-manifest. Default to parquet.
- **`references/multi-config.md`** — When to use multi-config (rare) and how (MMLU per-subject, FineWeb per-crawl, BhashaBench per-language patterns).
- **`references/quality-checklist.md`** — Pre-publication checklist. Run through it before declaring the dataset done.
- **`references/clarifying-questions.md`** — Questions to ask the user when intent is ambiguous.

## Bundled assets

- **`assets/example_features/`** — Ready-to-use feature specs (JSON) for the six canonical families: `instruction-tuning.json`, `chat.json`, `preference-dpo.json`, `pretraining.json`, `benchmark-mcq.json`, `benchmark-qa.json`. Copy one as your starting `features.json` and customize.
- **`assets/licenses/`** — Pre-written `LICENSE` text for `cc-by-4.0`, `cc-by-nc-4.0`, `mit`, `apache-2.0`. Copy the matching one into your dataset root.

## Bundled scripts

Run these from the project root. They are idempotent and re-runnable.

- **`scripts/produce_dataset.py`** — End-to-end pipeline: read input (JSONL/JSON/CSV/TSV with CSV type coercion), validate, build parquet shards, compute stats, write `stats.json`. Supports `--split-mode random|temporal|stratified`, `--drop-duplicates` (exact-dedup, recorded in stats.json), `--token-estimate` (heuristic chars/4 estimate), `--quiet` for CI, and writes empty shards for empty splits so README globs always match. Handles all feature types including `ClassLabel`, `Sequence`/`List` of scalars and structs, nested `struct`, and `Image`/`Audio`/`Video`. Use as a library or as a CLI.
- **`scripts/validate.py`** — Standalone validation suite (schema, dedup, PII, length, ClassLabel balance, contamination). Reports all PII types per field, Luhn-validates credit-card matches (fewer order-ID false positives), uses linear interpolation for percentiles, coerces CSV/TSV cells to declared dtypes, and keeps contextual PII patterns (IPv4, ISO dates, US ZIP) opt-in via `--pii-contextual`. Run on raw rows before sharding.
- **`scripts/make_card.py`** — Generate README.md from a feature spec + stats + example row. Supports `--auto-example` (extract first row from a parquet shard), `--namespace` is optional (omit for local-only datasets), and renders all feature types correctly including `ClassLabel` (with safe label escaping for YAML-hostile names) and `Sequence of struct`. Emits valid BibTeX (`\url` with a single backslash; empty authors are omitted).
- **`scripts/example_create_dataset.py`** — Template for the provenance script that ships with each dataset. **Self-contained** (no `import produce_dataset` — embeds the minimal pipeline inline) so it works as a standalone artifact in the dataset repo. Schema-aware quality filters. Copy into the dataset root as `create_dataset.py` and adapt.
- **`scripts/smoke_test.py`** — Post-build verification: loads the dataset via `load_dataset()`, verifies YAML parses, declared splits of the default config match (handles both single-config and multi-config `dataset_info` forms), ClassLabel `int2str()` works, the example row in `### Data Instances` matches the schema, and `LICENSE` + `create_dataset.py` are present. Run this before declaring the dataset done.

All scripts assume Python 3.10+ with `datasets`, `pyarrow`, `pyyaml` installed (tested with `datasets` 2.x–5.x, including 5.0, and `pyarrow` 14+). If missing: `pip install -r /home/z/my-project/skills/dataset-producer/requirements.txt`.

## Patterns observed in top datasets

These patterns are codified in the reference files — follow them rather than inventing your own:

1. **Parquet is the default.** Every modern top dataset (MMLU, GSM8K, UltraChat 200k, Alpaca, OASST, FineWeb) ships parquet. Use JSONL only for streaming exports or raw backups alongside parquet.
2. **Always declare `configs:` and `dataset_info:` in YAML** — even for single-config datasets (`config_name: default` is required). This makes the schema explicit and the Dataset Viewer works.
3. **The message-list chat schema** (`messages: list of {content, role}`) is the canonical format adopted by TRL, OpenAI, and Anthropic. Use it for chat. For DPO, use `{prompt, chosen: [...], rejected: [...]}`.
4. **One concrete JSON example in `### Data Instances`** is the single most useful section for users. Always include it.
5. **Commit the build script.** UltraFeedback Binarized and Argilla DPO pairs both ship `create_dataset.py`. Provenance is what makes a dataset trustworthy.
6. **Per-row provenance fields** (`id`, `url`, `date`, `source`, `language`, `language_score`, `token_count`) are how FineWeb and Dolma enable downstream filtering. Add them whenever the source is heterogeneous.
7. **BharatGen's BhashaBench pattern** for multilingual benchmarks: one config per domain, one split per language. Reuse this when the user needs multi-language or multi-domain benchmarks.

## Anti-patterns to avoid

- **Single JSON file for >1K rows** — slow to parse, doesn't stream. Use parquet or sharded JSONL.
- **Skipping `dataset_info`** — the loader infers it, but the Viewer may mis-detect types (e.g., ClassLabel becomes `int64`). Always declare explicitly.
- **No `LICENSE` file** — `license: cc-by-4.0` in YAML is metadata; the actual license text must be in the repo.
- **No example row in the card** — readers can't tell at a glance what the data looks like. Always include one in `### Data Instances`.
- **Hand-built parquet without sharding convention** — files like `train_data.parquet` won't be auto-loaded as the `train` split. Use `train-00000-of-00001.parquet`.
- **Auto-pushing to HF Hub without explicit user consent** — never do this. Always ask for the token and namespace.
- **No provenance script** — without `create_dataset.py`, no one can reproduce or audit the dataset. Always include one.

## Workflow summary

When the skill triggers:

1. Read the user's request and identify the dataset family + source.
2. If intent is ambiguous, ask 2-3 focused questions (see `references/clarifying-questions.md`).
3. Read `references/schemas.md` and pick the matching feature family.
4. Collect the raw rows (use `web-reader` for web sources, file reads for local sources, `LLM` for generation).
5. Run `scripts/validate.py` on the raw data; fix any issues.
6. Run `scripts/produce_dataset.py` to build parquet shards + stats. Pick the split mode that fits the data: `random` (default), `temporal` (preserve order), or `stratified` (balance a ClassLabel). Add `--drop-duplicates` if validate.py reported exact dupes, and `--token-estimate` if the user wants a quick token budget.
7. Run `scripts/make_card.py` to generate README.md. Use `--auto-example` to skip the manual example_row.json.
8. Copy a LICENSE file from `assets/licenses/`.
9. Adapt `scripts/example_create_dataset.py` into the dataset's `create_dataset.py` (the script is self-contained — copy it as-is and edit the constants/features/collect_rows/apply_filters blocks).
10. Save everything to `/home/z/my-project/download/<dataset_name>/`.
11. Run `scripts/smoke_test.py /home/z/my-project/download/<dataset_name>/` — fix anything that fails.
12. Run through `references/quality-checklist.md` — fix anything that fails.
13. Tell the user where the dataset is saved and what's in it.

The whole pipeline should produce a dataset that loads cleanly with `load_dataset("<path>")` and could be pushed to the Hub as-is.
