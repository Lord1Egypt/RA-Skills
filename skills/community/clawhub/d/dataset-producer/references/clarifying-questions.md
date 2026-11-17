# Clarifying Questions for Ambiguous Intent

> When the user's request is vague, ask 2-3 focused questions before writing any code. Don't ask all of them — pick the ones whose answers most change the dataset's structure.
>
> The goal is to nail down (1) the dataset family, (2) the source, (3) the splits, (4) the license, and (5) the size target. Everything else can be inferred or defaulted.

## The five essential dimensions

### 1. Family — what kind of dataset?

This determines the schema and the task categories. Ask when the user says "make a dataset" without specifying what for.

**Question**: "What kind of dataset do you want — instruction-following examples (SFT), multi-turn chat, preference pairs (DPO/RLHF), pretraining corpus, or a multiple-choice benchmark?"

**Options to suggest** (if the user is unsure):
- **Instruction-tuning (SFT)** — `(instruction, input, output)` triples. Use when you want to teach the model to follow single-turn instructions.
- **Chat** — multi-turn `messages: [{role, content}]`. Use when you want the model to converse.
- **Preference / DPO** — `(prompt, chosen, rejected)`. Use when you want the model to prefer one response over another (RLHF/DPO/ORPO training).
- **Pretraining corpus** — `(text, id, url, ...)` documents. Use when you want to train a base model from scratch.
- **Benchmark MCQ** — `(question, choices, answer)`. Use when you want to evaluate models on multiple-choice accuracy.
- **Benchmark QA** — `(question, context, answers)`. Use when you want to evaluate extractive QA.

### 2. Source — where does the data come from?

This determines the collection pipeline. Ask when the user hasn't said where the data is.

**Question**: "Where will the data come from — existing files (which format?), URLs to scrape, another dataset to transform, an LLM to generate it, or will you hand-write the rows?"

**Common answers**:
- "I have a folder of PDFs/CSVs/JSONL files" → read with `pypdf` / `pandas` / `json`, then build rows.
- "I want to scrape these URLs" → use the **web-reader** skill (`page_reader` for static pages, `agent-browser` for JS-rendered).
- "I want to derive it from `<existing-dataset>`" → `from datasets import load_dataset`.
- "I want the LLM to generate examples" → use the **LLM** skill to generate, then validate.
- "I'll write the rows by hand" → give me a CSV/JSON template; I'll fill the schema.

### 3. Splits — train/test/validation?

Ask when the user hasn't mentioned splits.

**Question**: "Should I split into train/test, or do you want train + validation + test, or just one split? What split ratio (e.g., 90/10, 80/10/10)?"

**Defaults**:
- Small (< 1K rows): train + test, 90/10. Skip validation.
- Medium (1K – 100K): train + validation + test, 80/10/10.
- Large (> 100K): train + test, 98/2 (validation can be carved out of train).
- Pretraining corpora: usually train only.
- Benchmarks: test + validation + (optional) `dev` for few-shot, often no train.

### 4. License — what can downstream users do with it?

Ask when the user hasn't said.

**Question**: "What license should the dataset be under? Default options: `cc-by-4.0` (attribution required, commercial OK), `apache-2.0` (code-friendly, commercial OK), `mit` (maximally permissive), `cc-by-nc-4.0` (non-commercial). Or do you have a specific license in mind?"

**Important**: the license must be compatible with the source data's license. If the user scraped copyrighted websites, they can't relicense as `cc-by-4.0`. Flag this when in doubt.

### 5. Size target — how many rows?

Ask when the user hasn't said.

**Question**: "Roughly how many rows do you want? This affects whether we need sharding and how long generation takes."

**Defaults**:
- Hand-curated: 100-1,000 rows
- SFT instruction-tuning: 1K-100K rows
- DPO preference: 1K-100K rows
- Pretraining corpus: 1M+ rows
- Benchmark: 100-10K rows (small enough to run cheaply)

## Optional dimensions (ask only if relevant)

### 6. Languages

**Question**: "What language(s) is the data in? (ISO 639-1 codes like `en`, `hi`, `zh`.)"

Skip if obvious from the source.

### 7. Multi-config / multi-domain

**Question**: "Should the dataset have multiple configs (e.g., one per domain, one per language, one per subject)?"

Default: single config. Multi-config only when the user genuinely needs subsets with different schemas or meanings (MMLU per-subject, FineWeb per-crawl, BhashaBench per-domain).

### 8. Output location

**Question**: "Where should I save the dataset — local directory (`/home/z/my-project/download/<name>/`) or push to the HuggingFace Hub (need your HF token + namespace)?"

Default: local. Only push to Hub if the user explicitly asks and provides a token.

### 9. Provenance level

**Question**: "Do you want full per-row provenance (source URL, fetch date, language score, token count)? Or just the data?"

Default: full provenance for pretraining corpora; minimal (just the data) for benchmarks.

### 10. Quality filters

**Question**: "Should I run PII scanning, dedup, contamination check, and language ID? Or just package the data as-is?"

Default: run all checks. Skip only if the user explicitly says "I just want to package the raw data."

## Pattern: 2-3 questions max

Don't dump all 10 questions on the user. Pick the 2-3 whose answers most change the dataset's structure:

| If user said | Ask these 2-3 |
|---|---|
| "Make a dataset" | Family, source, license |
| "Make a dataset from these PDFs" | Family, splits, license |
| "Make a benchmark" | What subject/domain, source (existing questions? generate?), license |
| "Make an SFT dataset" | Source (existing? generate? scrape?), size target, license |
| "Make a DPO dataset" | Source (LLM judge? human annotations?), splits, license |
| "Package this JSONL as a HF dataset" | Family (so I pick the right schema), license, splits (or just train?) |
| "Make a pretraining corpus from these URLs" | Languages, dedup (exact only or also fuzzy?), license |

## When NOT to ask

Skip the questions entirely if the user's request already pins down all five dimensions:

- "Make an SFT instruction-tuning dataset from `instructions.jsonl`, 90/10 train/test split, cc-by-4.0 license, ~5K rows" → all 5 dimensions specified, proceed.
- "Build an MMLU-style MCQ benchmark from `questions.csv` with 4-way choices, train+test, mit license" → all 5 specified.

If even one dimension is missing, ask. It's cheaper than producing the wrong dataset.
