# YAML Frontmatter Spec for HuggingFace Dataset README.md

> The YAML block at the top of `README.md` is delimited by `---` on its own line at the very start of the file. It serves two purposes: (a) **metadata for Hub discovery & filtering** (license, language, task, size) and (b) **loader configuration** (`configs`, `data_files`) plus **schema declaration** (`dataset_info`/`features`).
>
> This file is the complete reference. When generating a README.md, fill in every field you can — empty optional fields are fine, but missing required fields will break the loader or hide the dataset from Hub filters.

## Table of Contents

- [Minimal valid YAML](#minimal-valid-yaml)
- [Top-level fields (complete reference)](#top-level-fields-complete-reference)
- [`dataset_info` structure](#dataset_info-structure)
- [`features` field — type vocabulary](#features-field--type-vocabulary)
- [`configs` structure](#configs-structure)
- [`splits` block format](#splits-block-format)
- [`size_categories` buckets](#size_categories-buckets)
- [License identifiers](#license-identifiers)
- [`task_categories` and `task_ids` taxonomy](#task_categories-and-task_ids-taxonomy)
- [Hub limits and constraints](#hub-limits-and-constraints)
- [Common mistakes](#common-mistakes)

---

## Minimal valid YAML

For a single-config dataset with one parquet shard:

```yaml
---
license: cc-by-4.0
language:
  - en
pretty_name: My Dataset
size_categories:
  - 1K<n<10K
task_categories:
  - text-generation
configs:
  - config_name: default
    default: true
    data_files:
      - split: train
        path: data/train-*.parquet
      - split: test
        path: data/test-*.parquet
dataset_info:
  features:
    - name: instruction
      dtype: string
    - name: output
      dtype: string
  splits:
    - name: train
      num_examples: 5200
    - name: test
      num_examples: 500
  download_size: 1200000
  dataset_size: 2400000
---
```

That's the floor. Everything below is enrichment.

---

## Top-level fields (complete reference)

| Field | Type | Required? | Purpose |
|---|---|---|---|
| `license` | string **or** list of strings | recommended | SPDX identifier(s); see [License identifiers](#license-identifiers) |
| `language` | list of ISO 639-1 codes | recommended | `en`, `fr`, `zh`, … Discovery filter |
| `language_bcp47` | list of BCP-47 codes | optional | Finer-grained: `en-US`, `zh-CN`, `pt-BR` |
| `multilinguality` | list | optional | `monolingual`, `multilingual`, `translation`, `transliteration` |
| `language_creators` | list | optional | `crowdsourced`, `expert-generated`, `machine-generated`, `found`, `other` |
| `annotations_creators` | list | optional | Same vocabulary as `language_creators` + `no-annotation` |
| `source_datasets` | list | optional | `original`, `common-crawl`, `wikipedia`, … or `extended|<other-dataset>` |
| `task_categories` | list | recommended | Top-level ML task; see [taxonomy](#task_categories-and-task_ids-taxonomy) |
| `task_ids` | list | optional | Fine-grained sub-task |
| `size_categories` | string (one value, NOT a list) | recommended | Order-of-magnitude bucket; see [buckets](#size_categories-buckets) |
| `pretty_name` | string | recommended | Human-readable name shown in the Hub UI |
| `paperswithcode_id` | string | optional | Slug on PapersWithCode (`mmlu`, `gsm8k`) |
| `tags` | list | optional | Free-form tags. Special values trigger UI behavior: `argilla`, `dask`, `datasets`, `distilabel`, `fiftyone`, `mlcroissant`, `pandas`, `webdataset` (associate a library); `3d`, `audio`, `geospatial`, `image`, `tabular`, `text`, `timeseries`, `video` (force modality) |
| `configs` | list | required for non-trivial layouts | Loader config: maps `config_name` → `data_files`. See [`configs` structure](#configs-structure) |
| `dataset_info` | list **or** dict | recommended | Per-config feature schema + split stats. See [`dataset_info` structure](#dataset_info-structure) |
| `viewer` | bool | optional | `false` to disable the Dataset Viewer (huge corpora like Dolma) |

**Best practice**: declare both `configs` and `dataset_info` so the schema is explicit even if a shard is missing.

---

## `dataset_info` structure

Two valid shapes:

### A. Single-config (dict form)

Used by UltraChat 200k, UltraFeedback Binarized, Alpaca, OASST1/2.

```yaml
dataset_info:
  features:
    - name: prompt
      dtype: string
    - name: messages
      list:
        - name: content
          dtype: string
        - name: role
          dtype: string
  splits:
    - name: train_sft
      num_bytes: 1397058554
      num_examples: 207865
    - name: test_sft
      num_bytes: 154695659
      num_examples: 23110
  download_size: 1624049723      # bytes of the on-disk files (post-compression)
  dataset_size: 3047427114       # bytes once loaded into memory (Arrow decoded)
```

### B. Multi-config (list form)

Used by MMLU, GSM8K, FineWeb.

```yaml
dataset_info:
  - config_name: abstract_algebra
    features:
      - name: question
        dtype: string
      - name: subject
        dtype: string
      - name: choices
        sequence: string
      - name: answer
        dtype:
          class_label:
            names:
              '0': A
              '1': B
              '2': C
              '3': D
    splits:
      - name: test
        num_bytes: 49618.67
        num_examples: 100
      - name: validation
        num_bytes: 5485.52
        num_examples: 11
      - name: dev
        num_bytes: 2199.18
        num_examples: 5
    download_size: 17143
    dataset_size: 57303.36
  - config_name: all
    features: ...                # same feature block
    splits:
      - name: test
        num_examples: 14042
```

Each `config_name` entry can have its own `features` block — configs may have different schemas.

---

## `features` field — type vocabulary

`features` is a list of `- name: <col>` + a type spec. The type spec can be:

| YAML key | Python equivalent | Meaning |
|---|---|---|
| `dtype: string` / `int32` / `int64` / `float32` / `float64` / `bool` / `binary` | `Value("string")` etc. | Scalar `Value` |
| `dtype: uint32` / `uint64` | `Value("uint32")` | Unsigned integer |
| `dtype: timestamp[ms]` (also `s`, `us`, `ns`) | `Value("timestamp[ms]")` | Timestamp |
| `sequence: <dtype_or_struct>` | `Sequence(Value(...))` | `Sequence` of a scalar |
| `list:` (with nested `- name:` blocks) | `Sequence({...})` | `Sequence` of a struct |
| `struct:` (with nested `- name:` blocks) | `{...}` | Nested dict feature |
| `dtype: class_label:` + `names:` | `ClassLabel(names=[...])` | Categorical (stored as int) |
| `dtype:` with `_type: Image` | `Image()` | Image feature (PIL on load) |
| `dtype:` with `_type: Audio` + `sampling_rate:` | `Audio(sampling_rate=...)` | Audio feature |
| `dtype:` with `_type: Video` | `Video()` | Video feature |
| `dtype:` with `_type: Pdf` | `Pdf()` | PDF document |
| `array2d:` / `array3d:` / `array4d:` / `array5d:` + `shape:` + `dtype:` | `Array2D` / `Array3D` / … | Fixed/var-length arrays (first dim can be `null`) |
| `sequence:` of `sequence:` | `Sequence(Sequence(...))` | Nested list (e.g. tokenized text) |
| `large_list:` | `LargeList` | Very large variable-length lists |
| `translation:` | `Translation()` | Translation pair feature |
| `translation_variable_languages:` | `TranslationVariableLanguages()` | Variable-language pairs |

### Examples

**Scalar:**
```yaml
- name: instruction
  dtype: string
```

**Sequence of scalars:**
```yaml
- name: choices
  sequence: string
```

**List of structs (chat messages):**
```yaml
- name: messages
  list:
    - name: content
      dtype: string
    - name: role
      dtype: string
```

**Nested struct (toxicity scores):**
```yaml
- name: detoxify
  struct:
    - name: toxicity
      dtype: float64
    - name: severe_toxicity
      dtype: float64
    - name: obscene
      dtype: float64
```

**ClassLabel:**
```yaml
- name: answer
  dtype:
    class_label:
      names:
        '0': A
        '1': B
        '2': C
        '3': D
```

The richer form used by the `datasets` Python API serializes as `dtype: string, _type: Value` etc., but in hand-written YAML you can use the short forms above — the loader accepts both.

---

## `configs` structure

```yaml
configs:
  - config_name: default                # required, even for single config
    default: true                       # optional: which config loads with no name
    data_files:                         # option A: explicit split→path mapping
      - split: train
        path: "data/train-*.parquet"    # glob; or list of paths
      - split: test
        path:
          - "data/test-00000-of-00001.parquet"
          - "data/extra_test.parquet"
    # OR option B: point at a directory (split inferred from filenames inside)
    # data_dir: "data"
    # OR option C: single path / glob (no split key — becomes single 'train' split)
    # data_files: "data/all.parquet"
    # Optional builder params:
    sep: "\t"                           # csv builder
    features:                           # override features per config
      ...
```

### Multi-config example (GSM8K — 2 configs)

```yaml
configs:
  - config_name: main
    data_files:
      - split: train
        path: main/train-*
      - split: test
        path: main/test-*
  - config_name: socratic
    data_files:
      - split: train
        path: socratic/train-*
      - split: test
        path: socratic/test-*
```

### Multi-config example (FineWeb — one config per CommonCrawl dump)

```yaml
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/*/*
  - config_name: sample-10BT
    data_files:
      - split: train
        path: sample/10BT/*
  - config_name: CC-MAIN-2024-51
    data_files:
      - split: train
        path: data/CC-MAIN-2024-51/*
```

### Multi-config example (BharatGen BhashaBench-Multi — one config per domain, one split per language)

```yaml
configs:
  - config_name: BBA           # BhashaBench Ayur
    data_files:
      - split: english
        path: bhashabench_ayur/en.parquet
      - split: hindi
        path: bhashabench_ayur/hi.parquet
      - split: tamil
        path: bhashabench_ayur/ta.parquet
      # ... one per language
```

This lets users `load_dataset("repo", "BBA", split="hindi")` to get the Hindi Ayurveda questions directly.

---

## `splits` block format

```yaml
splits:
  - name: train                 # required
    num_bytes: 1397058554       # optional but recommended — bytes after Arrow decoding
    num_examples: 207865        # optional but recommended — row count
    dataset_name: null          # optional — internal use
  - name: test
    num_bytes: 154695659
    num_examples: 23110
```

At the `dataset_info` (per-config) level, also state aggregate stats:

```yaml
download_size: 1624049723       # bytes of the on-disk files (post-compression)
dataset_size: 3047427114        # bytes in memory after decoding (>= download_size for compressed formats)
```

These power the size badges and the "X rows" indicator on the Hub.

### How the loader infers splits (when YAML doesn't declare them)

Three mechanisms, in order of precedence:

1. **Explicit YAML** (highest precedence, recommended for anything non-trivial) — see above.
2. **Filename inference**. The loader scans file names for split keywords separated by non-word characters (`_`, `-`, `.`, space, digits):
   - `train` ← `train.csv`, `my_train_file.csv`, `train1.csv`, `train_0.parquet`
   - `validation` ← `validation`, `valid`, `val`, `dev`
   - `test` ← `test`, `testing`, `eval`, `evaluation`
3. **Directory-name inference**: `train/`, `test/`, `validation/` directories — split is inferred from the directory name.
4. **Custom split names** via the `<split_name>-XXXXX-of-XXXXX.parquet` pattern (e.g., `random-00000-of-00003.parquet` creates a `random` split).
5. **Fallback**: if nothing matches, all files become a single `train` split.

Always declare explicitly when in doubt.

---

## `size_categories` buckets

Single value (NOT a list):

| Value | Meaning |
|---|---|
| `n<1K` | fewer than 1,000 examples |
| `1K<n<10K` | 1K – 10K |
| `10K<n<100K` | 10K – 100K |
| `100K<n<1M` | 100K – 1M |
| `1M<n<10M` | 1M – 10M |
| `10M<n<100M` | 10M – 100M |
| `100M<n<1B` | 100M – 1B |
| `1B<n<10B` | 1B – 10B |
| `10B<n<100B` | 10B – 100B |
| `100B<n<1T` | 100B – 1T |
| `n>1T` | more than 1T (Dolma, FineWeb) |
| `unknown` | not yet computed |

Pick the bucket that contains your total row count across all splits.

---

## License identifiers

Use SPDX identifiers (single string) or a list of SPDX strings. The Hub displays the license if the key matches its license table. Common keys:

| Key | License |
|---|---|
| `mit` | MIT |
| `apache-2.0` | Apache 2.0 |
| `cc-by-4.0` | Creative Commons Attribution 4.0 |
| `cc-by-sa-4.0` | CC Attribution-ShareAlike 4.0 |
| `cc-by-nc-4.0` | CC Attribution-NonCommercial 4.0 (Alpaca) |
| `cc-by-nc-sa-4.0` | CC Attribution-NonCommercial-ShareAlike 4.0 |
| `cc0-1.0` | CC0 / Public Domain Dedication |
| `cc-by-2.0` / `cc-by-3.0` | older CC versions |
| `odc-by` | Open Data Commons Attribution (Dolma, FineWeb) |
| `bsd-3-clause` / `bsd-2-clause` | BSD |
| `gpl-3.0` / `lgpl-3.0` / `agpl-3.0` | GPL family |
| `mpl-2.0` | Mozilla Public License |
| `afl-3.0` | Academic Free License |
| `unlicense` | The Unlicense |
| `cdla-sharing-1.0` / `cdla-permissive-2.0` | Community Data License Agreement |
| `other` / `unknown` | catch-alls when nothing fits |

When the dataset is multi-licensed (e.g., different sources under different terms), use a list: `license: [cc-by-4.0, mit]`.

### Default recommendations

If you're unsure what to pick:

- **`cc-by-4.0`** — most permissive data license with attribution. Use this by default for openly-collected data.
- **`apache-2.0`** — code-friendly; use if the dataset includes a build script you want people to freely reuse.
- **`mit`** — maximally permissive; good for small hand-curated datasets.
- **`cc-by-nc-4.0`** — non-commercial; use if the source data is NC-licensed (e.g., Alpaca's underlying text-davinci-003 outputs).
- **`odc-by`** — for large crawled corpora (Dolma, FineWeb use this).
- **`other`** — only if the source has a custom license. Add a sentence in the README explaining the situation.

Always include the matching `LICENSE` file in the repo root.

---

## `task_categories` and `task_ids` taxonomy

`task_categories` is a list of **top-level ML tasks** (the same vocabulary used by the Hub's "Tasks" sidebar).

### NLP

- `text-generation`, `text-classification`, `token-classification`, `question-answering`, `fill-mask`, `summarization`, `translation`, `multiple-choice`, `text2text-generation`, `conversational`, `table-question-answering`, `zero-shot-classification`, `sentence-similarity`

### Audio

- `text-to-speech`, `automatic-speech-recognition`, `audio-classification`, `audio-to-audio`, `voice-activity-detection`

### Vision

- `image-classification`, `image-segmentation`, `object-detection`, `image-to-text`, `text-to-image`, `image-to-image`, `unconditional-image-generation`, `depth-estimation`, `video-classification`, `zero-shot-image-classification`, `mask-generation`

### Tabular

- `tabular-classification`, `tabular-regression`, `tabular-to-text`

### Multimodal / RL

- `reinforcement-learning`, `robotics`, `text-to-video`, `visual-question-answering`, `document-question-answering`, `graph-ml`

### Other

- `time-series-forecasting`, `feature-extraction`, `structured-prediction`, `anomaly-detection`, `other`

### `task_ids` (fine-grained sub-task IDs)

Each refines one task category:

| `task_category` | Possible `task_ids` |
|---|---|
| `question-answering` | `multiple-choice-qa`, `extractive-qa`, `open-domain-qa`, `closed-domain-qa` |
| `text-classification` | `multi-label-classification`, `multi-class-classification`, `sentiment-analysis`, `topic-classification`, `natural-language-inference`, `semantic-similarity-scoring` |
| `text-generation` | `language-modeling`, `dialogue-generation`, `text-simplification` |
| `summarization` | `news-articles-summarization`, `news-articles-headline-generation`, `multilingual-summarization` |
| `translation` | `machine-translation` |
| `multiple-choice` | `multiple-choice-qa` |
| `token-classification` | `named-entity-recognition`, `part-of-speech` |

GSM8K uses `task_categories: [text-generation]` with `task_ids: []` (empty). MMLU uses `task_categories: [question-answering]` with `task_ids: [multiple-choice-qa]`.

### Mapping dataset families to task categories

| Dataset family | `task_categories` | `task_ids` |
|---|---|---|
| Instruction-tuning | `text-generation`, `text2text-generation` | `language-modeling`, `dialogue-generation` |
| Chat | `conversational`, `text-generation` | `dialogue-generation` |
| Preference/DPO | `reinforcement-learning`, `text-generation` | (often empty) |
| Pretraining | `text-generation` | `language-modeling` |
| Benchmark MCQ | `question-answering`, `multiple-choice` | `multiple-choice-qa` |
| Benchmark QA | `question-answering` | `extractive-qa` or `open-domain-qa` |

---

## Hub limits and constraints

| Limit | Value | Notes |
|---|---|---|
| Per-file hard limit | 200 GB | LFS |
| Per-file recommended | < 50 GB | |
| Per-folder recommended | < 10,000 files | Git performance threshold |
| Per-repo soft cap (public) | 300 GB | Contact HF for larger |
| `viewer_row_size_mb` | 2 MB | Keep individual rows under ~2 MB so the Viewer can sample them (matters for image/audio/embedding columns) |

### Sharding strategy

- Aim for **1–5 GB per shard** for medium datasets (matches `push_to_hub(max_shard_size="1GB")`).
- For petabyte-scale corpora (FineWeb), use ~2 GB shards across hundreds of subdirectories partitioned by source/date.
- For multi-config datasets, either (a) **one directory per config** (`main/`, `socratic/`) or (b) **flat with split name in file** (`train_sft-00000-of-00003.parquet`).
- For huge corpora where even sharded parquet is too big to host, use the **Dolma pattern**: repo holds only a `urls/vX.txt` manifest + loader script; data lives in object storage.

### Naming convention (mandatory for auto-load)

```
<split>-<NNNNN>-of-<NNNNN>[-<hash>].parquet
```

- `<split>`: `train`, `test`, `validation`, or custom (`train_sft`, `train_prefs`).
- `<NNNNN>-of-<NNNNN>`: shard index zero-padded to 5 digits, total shard count zero-padded to 5 digits.
- `<hash>` (optional): 16-hex content hash added by `push_to_hub()` for cache-busting / content addressing. Drop it for hand-built shards.

---

## Common mistakes

1. **`size_categories` as a list** — it's a single string, not a list. `size_categories: 1K<n<10K`, not `size_categories: [1K<n<10K]`.

2. **Missing `config_name` for single-config datasets** — even single-config datasets need `config_name: default`. The loader requires it.

3. **`ClassLabel` stored as `string`** — `ClassLabel` is stored as `int` internally. Declare it as:
   ```yaml
   dtype:
     class_label:
       names:
         '0': A
         '1': B
   ```
   Not as `dtype: string`. The Viewer renders dropdowns only for ClassLabel.

4. **Glob patterns that match nothing** — if `path: data/train-*.parquet` matches no files, the loader fails. Verify your shards exist before publishing.

5. **No `LICENSE` file** — `license: cc-by-4.0` in YAML is metadata; the actual license text must be in the repo root as `LICENSE` (or `LICENSE.md`, `LICENSE.txt`).

6. **Wrong `download_size` / `dataset_size`** — `download_size` is the on-disk compressed bytes (sum of parquet file sizes); `dataset_size` is the in-memory Arrow decoded bytes (always ≥ `download_size` for compressed formats). Compute them; don't guess.

7. **`viewer: false` for small datasets** — only set `viewer: false` for petabyte-scale corpora where the Viewer can't pre-process. For normal datasets, the Viewer is a major discovery feature; don't disable it.

8. **No example row in `### Data Instances`** — this is the single most useful section for users. Always include one concrete JSON example.

9. **Custom split names that collide with reserved keywords** — avoid `train_test`, `validation_train`, etc. Use suffixes like `train_sft`, `train_prefs` instead.

10. **Forgetting `default: true`** — when there are multiple configs, mark one as `default: true` so the Viewer shows it first. Single-config datasets don't need this.
