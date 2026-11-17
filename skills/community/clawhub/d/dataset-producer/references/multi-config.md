# Multi-Config Datasets — When and How

> Most datasets have a single config (`default`). Multi-config is for when you genuinely need subsets with **different schemas**, **different sources**, or **different domains/languages**. Don't add a config layer unless it carries real meaning — it adds friction for the user (they have to know the config name to load the data).

## When to use multi-config

Use multi-config when one of these is true:

1. **Different schemas per subset** — e.g., MMLU has 57 subjects but they all share a schema, so it's still multi-config for navigation, not because schemas differ. (Use multi-config for navigation.)
2. **Per-domain benchmark** — BhashaBench has 4 configs (`BBA`, `BBK`, `BBF`, `BBL`) for Ayurveda, Agriculture, Finance, Law. Users want to load just one domain.
3. **Per-language benchmark** — FineWeb has one config per CommonCrawl dump; BhashaBench-Multi uses one split per language.
4. **Per-source pretraining corpus** — Dolma has versions (v1, v1.5, v1.6, v1.7) which are exposed as separate config_names.
5. **Sample vs full** — FineWeb ships `sample-10BT`, `sample-100BT`, `sample-350BT` alongside the full corpus so users can prototype cheaply.

## When NOT to use multi-config

- Just to organize files internally — use directories instead.
- For train/test split — those are **splits**, not configs.
- For different formats (parquet vs jsonl) — pick one and stick with it.
- For versioning — use git tags / HF revisions instead.

## Two valid file layouts

### Pattern A: One directory per config

Used by MMLU, GSM8K, FineWeb. Each config has its own directory containing parquet files:

```
my_dataset/
├── README.md
├── data/
│   ├── main/                                # config_name: main
│   │   ├── train-00000-of-00001.parquet
│   │   └── test-00000-of-00001.parquet
│   └── socratic/                            # config_name: socratic
│       ├── train-00000-of-00001.parquet
│       └── test-00000-of-00001.parquet
```

YAML:
```yaml
configs:
  - config_name: main
    default: true
    data_files:
      - split: train
        path: data/main/train-*
      - split: test
        path: data/main/test-*
  - config_name: socratic
    data_files:
      - split: train
        path: data/socratic/train-*
      - split: test
        path: data/socratic/test-*
```

### Pattern B: Flat with config name in filename

Used by BhashaBench-Multi. All files live in one directory, with the config name encoded in the filename:

```
my_dataset/
├── README.md
├── bhashabench_ayur/
│   ├── en.parquet
│   ├── hi.parquet
│   ├── ta.parquet
│   └── ...
├── bhashabench_finance/
│   ├── en.parquet
│   └── ...
```

YAML:
```yaml
configs:
  - config_name: BBA
    data_files:
      - split: english
        path: bhashabench_ayur/en.parquet
      - split: hindi
        path: bhashabench_ayur/hi.parquet
      # ... one per language
```

This pattern uses **split name = language name** (BharatGen's convention), which is unusual but lets users `load_dataset("repo", "BBA", split="hindi")`.

### Pattern C: One split per config (rare)

When each config is itself a single split (e.g., a "small" sample and a "full" version):

```yaml
configs:
  - config_name: full
    default: true
    data_files:
      - split: train
        path: data/full/train-*.parquet
  - config_name: sample-10BT
    data_files:
      - split: train
        path: data/sample-10BT/train-*.parquet
```

## `dataset_info` for multi-config

Use the **list form** (one `- config_name:` entry per config):

```yaml
dataset_info:
  - config_name: main
    features:
      - name: question
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
      - name: train
        num_examples: 7473
      - name: test
        num_examples: 1319
    download_size: 2200000
    dataset_size: 2600000
  - config_name: socratic
    features: ...                # same or different feature block
    splits:
      - name: train
        num_examples: 7473
      - name: test
        num_examples: 1319
    download_size: 2600000
    dataset_size: 3000000
```

## BharatGen BhashaBench pattern (multilingual MCQ)

For multilingual benchmarks where each language is its own split:

```yaml
configs:
  - config_name: BBA                              # BhashaBench Ayur
    data_files:
      - split: english
        path: bhashabench_ayur/en.parquet
      - split: hindi
        path: bhashabench_ayur/hi.parquet
      - split: tamil
        path: bhashabench_ayur/ta.parquet
      - split: telugu
        path: bhashabench_ayur/te.parquet
      # ... one per language (22 Indic languages + English = 23 splits per config)
  - config_name: BBF                              # BhashaBench Finance
    data_files:
      - split: english
        path: bhashabench_finance/en.parquet
      # ...
  - config_name: BBK                              # BhashaBench Krishi (Agriculture)
    data_files: ...
  - config_name: BBL                              # BhashaBench Legal
    data_files: ...
```

Users then load specific subsets:

```python
from datasets import load_dataset

# All Hindi Ayurveda questions
ds = load_dataset("bharatgenai/BhashaBench-Multi", "BBA", split="hindi")

# All Tamil Finance questions
ds = load_dataset("bharatgenai/BhashaBench-Multi", "BBF", split="tamil")
```

This pattern is powerful for multilingual benchmarks because:
- Users don't have to download the entire 1.7 GB corpus to evaluate one language
- Per-language evaluation is a single `load_dataset` call
- Adding a new language is just adding a new split + parquet file

## Tooling notes

- The HF Dataset Viewer shows the `default: true` config first; users can switch via a dropdown.
- `load_dataset("repo")` without a config name loads the `default: true` config.
- For multi-config datasets with very different schemas per config, document each config's schema in the README's `### Data Instances` section (show one example per config).
- If a config has a different schema from the others, declare its `features` explicitly in its `dataset_info` entry — don't rely on inference.

## Decision tree

```
Does the user need to load subsets independently?
├── NO  → single config (`default`)
└── YES → multi-config
    What's the subset dimension?
    ├── Domain (e.g., Ayur / Finance / Legal) → one config per domain
    ├── Language (e.g., en / hi / ta)        → one split per language (BhashaBench pattern)
    ├── Source (e.g., CC dump)               → one config per source (FineWeb pattern)
    └── Sample size (e.g., 10BT / 100BT)     → one config per sample size
```

If the subset dimension is language AND there are < 5 languages, you can also use one config with a `language` column — but the BhashaBench "split per language" pattern is more idiomatic for > 10 languages.
