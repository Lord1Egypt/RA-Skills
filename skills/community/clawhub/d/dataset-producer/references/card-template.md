# Dataset Card Template (README.md)

> Copy this template, fill in the placeholders (`<...>`), and delete any section that genuinely doesn't apply. Fill every section you can — use `[More Information Needed]` only as a last resort for fields you genuinely can't fill.
>
> The YAML frontmatter goes at the very top, delimited by `---`. The markdown body follows.

---

## Full template

```markdown
---
license: <spdx-id>                              # e.g. cc-by-4.0, apache-2.0, mit, cc-by-nc-4.0
language:                                       # list of ISO 639-1 codes
  - en
  - hi
pretty_name: <Human-Readable Dataset Name>      # shown in Hub UI
size_categories: <bucket>                       # single value: n<1K, 1K<n<10K, 10K<n<100K, 100K<n<1M, 1M<n<10M, ...
task_categories:                                # see yaml-spec.md taxonomy
  - text-generation
task_ids:                                       # optional fine-grained sub-tasks
  - language-modeling
language_creators:                              # optional
  - machine-generated
annotations_creators:                           # optional
  - machine-generated
source_datasets:                                # optional
  - original
tags:                                           # optional free-form tags
  - <domain>
  - <subdomain>

configs:                                        # required even for single config
  - config_name: default
    default: true
    data_files:
      - split: train
        path: data/train-*.parquet
      - split: test
        path: data/test-*.parquet
      - split: validation
        path: data/validation-*.parquet

dataset_info:                                   # recommended — declares schema explicitly
  features:
    - name: <field1>
      dtype: string
    - name: <field2>
      dtype: string
    # ... add a - name: block for every column
  splits:
    - name: train
      num_bytes: <bytes>
      num_examples: <count>
    - name: test
      num_bytes: <bytes>
      num_examples: <count>
  download_size: <bytes>                        # sum of parquet file sizes on disk
  dataset_size: <bytes>                         # in-memory Arrow decoded bytes (>= download_size)
---

# Dataset Card for <Dataset Name>

## Table of Contents

- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** <url or "N/A">
- **Repository:** <url or "N/A">
- **Paper:** <arxiv/url or "N/A">
- **Leaderboard:** <url or "N/A">
- **Point of Contact:** <email or "N/A">

### Dataset Summary

<1–3 paragraphs: what the dataset is, how many examples, why it exists. Cover:
- What the dataset contains (modality, topic, structure)
- Total size (rows, tokens, or files)
- Why it was created (gap it fills, intended use)
- How it was produced (LLM-generated, crowd-sourced, crawled, transformed from existing dataset)>

### Supported Tasks and Leaderboards

<List ML tasks the dataset supports, e.g. "text-generation (instruction-following SFT), text2text-generation, evaluation of multilingual MCQ accuracy". If the dataset appears on a leaderboard (e.g. HF Open LLM Leaderboard), name it.>

### Languages

<List BCP-47 codes + plain-language description. E.g. "English (en). The dataset is monolingual; there are no translations." or "23 languages: English (en), Hindi (hi), Tamil (ta), ... ">

## Dataset Structure

### Data Instances

A single example from the dataset:

```json
{
  "<field1>": "<value>",
  "<field2>": "<value>",
  ...
}
```

<One sentence explaining what this row represents.>

### Data Fields

<List each column with name, type, and meaning.>

- `<field1>` (`string`): <one-line description>
- `<field2>` (`string`): <one-line description>
- `<field3>` (`list of {role, content}`): <description>
- ...

### Data Splits

| Split | Num Examples |
|---|---|
| `train` | <count> |
| `test` | <count> |
| `validation` | <count> |

<Optional: explain the split rationale — random split, temporal split, held-out test set, etc.>

## Dataset Creation

### Curation Rationale

<Why was this dataset built? What gap does it fill? What design choices were made? E.g. "Built on Self-Instruct with text-davinci-003, 175 seed tasks expanded to 52K, $500 cost. Differs from Self-Instruct in (X, Y, Z).">

### Source Data

#### Initial Data Collection and Normalization

<Where the raw data came from; what cleaning was done. For crawled data: which sources, time range, dedup/PII/quality filters applied. For generated data: which model, which prompt template, generation params. For crowd-sourced: platform, payment, qualification criteria.>

#### Who are the source language producers?

<For crawled data: demographics of original authors (often unknown). For generated: which LLM and its known biases. For crowd-sourced: annotator demographics if known.>

### Annotations

#### Annotation process

<How labels/scores were produced. For LLM-judged: judge model, judge prompt, rating scale. For crowd-sourced: task instructions, review process, inter-annotator agreement. For automated: which classifier, threshold, false-positive handling.>

#### Who are the annotators?

<Annotator demographics, pay, training, language proficiency. For LLM-judged: which model and version.>

### Personal and Sensitive Information

<PII scan results. State whether regex-based scan, presidio, or other PII detection was run, and the result. Describe the removal-request process if applicable.>

## Considerations for Using the Data

### Social Impact of Dataset

<Risks, dual-use concerns, intended-use statement. What could go wrong if the dataset is misused?>

### Discussion of Biases

<Known biases: gender, racial, cultural, political, linguistic. Don't claim "no biases" — every dataset has them.>

### Other Known Limitations

<Coverage gaps, annotation noise, contamination, temporal drift. Be honest.>

## Additional Information

### Dataset Curators

<People/orgs responsible. E.g. "Built by <name> at <org>. Contact: <email>.">

### Licensing Information

<SPDX code + link to full text. E.g. "Creative Commons Attribution 4.0 (CC-BY-4.0). See [LICENSE](LICENSE) for the full text.">

### Citation Information

If you use this dataset, please cite:

```bibtex
@misc{<citation_key>,
  title         = {<Dataset Title>},
  author        = {<Author 1> and <Author 2> and ...},
  year          = {<YYYY>},
  howpublished  = {\url{https://huggingface.co/datasets/<namespace>/<name>}},
  note          = {<optional version note>},
}
```

### Contributions

Thanks to [@github-username](https://github.com/<github-username>) for adding this dataset.
```

---

## What each section is for

| Section | Purpose | Real-world example |
|---|---|---|
| **Dataset Description** (top-level list) | One-line links: Homepage, Repository, Paper, Leaderboard, Point of Contact | GSM8K README lists `https://openai.com/blog/grade-school-math/`, the GitHub repo, the arXiv link |
| **Dataset Summary** | 1–3 paragraphs: what / how many / why | Alpaca: "52,000 instructions and demonstrations generated by OpenAI's `text-davinci-003`" + how the pipeline differs from Self-Instruct |
| **Supported Tasks and Leaderboards** | Which ML tasks the dataset supports; which leaderboard(s) it appears on | GSM8K: "test logic and math in language modelling … used for the LLM Leaderboard" |
| **Languages** | BCP-47 codes + plain-language description | GSM8K: "English. The associated BCP-47 code is `en`" |
| **Data Instances** | A concrete JSON example of one row, in a fenced ```json block. **The single most useful section for users.** | Alpaca shows a 4-key JSON object; GSM8K shows the `main` and `socratic` configs side by side |
| **Data Fields** | Bullet list of each column: name, type, meaning | Alpaca lists `instruction`, `input`, `output`, `text` with one-line semantics |
| **Data Splits** | Markdown table of split → row counts | UltraChat 200k: `| train_sft | test_sft | train_gen | test_gen |` with counts `207865 | 23110 | 256032 | 28304` |
| **Curation Rationale** | Why was this dataset built, what gap does it fill | Alpaca: built on Self-Instruct with text-davinci-003, $500 cost, 52K examples |
| **Source Data / Initial Data Collection and Normalization** | Where the raw data came from; what cleaning was done | FineWeb: CommonCrawl → datatrove pipeline (extraction, fuzzy dedup, quality filtering) |
| **Source Data / Who are the source language producers?** | Demographics of original authors | Often `[More Information Needed]` for crawled data |
| **Annotations / Annotation process** | How labels/scores were produced | OASST1: crowd-sourced on open-assistant.io, 13,500 volunteers, quality ratings + spam/lang/PII labels |
| **Annotations / Who are the annotators?** | Annotator demographics, pay, training | OASST1: worldwide volunteers |
| **Personal and Sensitive Information** | PII scan results, removal request process | Dolma: links to a Google Form for PII removal |
| **Social Impact of Dataset** | Risks, dual-use concerns | Alpaca: quotes the official release blog post about risk/benefit tradeoff |
| **Discussion of Biases** | Known biases (gender, racial, cultural, political) | Often `[More Information Needed]` |
| **Other Known Limitations** | Coverage gaps, annotation noise, contamination | Alpaca: "generated by a language model and inevitably contains some errors or biases" |
| **Dataset Curators** | People/orgs responsible | Often the namespace owner |
| **Licensing Information** | SPDX license + link to full text | Alpaca: "Creative Commons NonCommercial (CC BY-NC 4.0)" |
| **Citation Information** | BibTeX block | UltraChat 200k includes the `@misc{ding2023enhancing, …}` block |
| **Contributions** | GitHub handles of contributors | `Thanks to [@github-username] for adding this dataset.` |

---

## Variations seen in the wild

The template is a **recommendation, not a strict requirement**. Top datasets commonly:

- **Drop sections** that don't apply (UltraChat 200k's README is just `# Dataset Card` → `## Dataset Description` → `## Dataset Structure` → `## Citation`).
- **Add a `## Using this dataset`** section with `load_dataset(...)` snippets (Argilla distilabel DPO pairs).
- **Add a `## Reproducing the dataset`** section with the processing script (Argilla distilabel DPO, UltraFeedback Binarized links to `create_dataset.py`).
- **Add a `## Versions`** section (Dolma: table of v1, v1.5, v1.6, v1.7 with release dates and sizes).
- **Add a `## Summary Statistics`** section (Dolma, FineWeb: per-source tables of doc counts and token counts).
- **Add a `## Download`** section (Dolma: parallel `wget` recipe).

Use your judgment: keep the canonical sections, add custom sections only when they carry real information.

---

## Hub-specific markdown features

- A YAML-broken link to an arXiv abstract or HF paper page is auto-detected and surfaces an `arxiv:<id>` tag on the dataset page.
- Force the modality tag by adding `3d`, `audio`, `geospatial`, `image`, `tabular`, `text`, `timeseries`, or `video` under `tags:`.
- Associate a loading library (`argilla`, `dask`, `datasets`, `distilabel`, `fiftyone`, `mlcroissant`, `pandas`, `webdataset`) by adding it under `tags:`.

---

## Minimal acceptable card (when the user is in a hurry)

If the user wants a quick-and-dirty dataset, this is the absolute minimum that still loads and is useful:

```markdown
---
license: cc-by-4.0
language:
  - en
pretty_name: <Name>
size_categories: 1K<n<10K
task_categories:
  - text-generation
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train-*.parquet
dataset_info:
  features:
    - name: <field1>
      dtype: string
    - name: <field2>
      dtype: string
  splits:
    - name: train
      num_examples: <count>
  download_size: <bytes>
  dataset_size: <bytes>
---

# Dataset Card for <Name>

## Dataset Summary

<2–3 sentences.>

## Data Instances

```json
{
  "<field1>": "<value>",
  "<field2>": "<value>"
}
```

## Data Fields

- `<field1>` (`string`): <description>
- `<field2>` (`string`): <description>

## Licensing Information

[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE).

## Citation Information

```bibtex
@misc{<key>,
  title = {<Name>},
  author = {<Author>},
  year = {<YYYY>},
  url = {https://huggingface.co/datasets/<namespace>/<name>}
}
```
```

But strongly prefer the full template — the missing sections (especially **Curation Rationale**, **Annotations**, **Personal and Sensitive Information**, **Discussion of Biases**) are what make a dataset trustworthy.
