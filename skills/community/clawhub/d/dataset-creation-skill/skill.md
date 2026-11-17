---
name: dataset-creation-training
description: End-to-end workflow for building, cleaning, annotating, splitting, and training on custom datasets. Covers data collection, quality assurance, format standardization (Alpaca, ShareGPT, ChatML, JSONL), synthetic data generation, train/val/test splitting, and training integration. Use when the user wants to "create a dataset", "prepare training data", "fine-tune a model", "clean data for ML", or "generate synthetic examples".
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
      anyBins:
        - pandas
        - datasets
    emoji: "📊"
    homepage: https://clawhub.ai/skills/dataset-creation-training
    os:
      - linux
      - macos
---

# Dataset Creation & Training

Complete guide for building high-quality datasets and training models. Quality data consistently outperforms model size and hyperparameter tuning — this skill covers the full lifecycle from raw collection to trained model.

## When to Use

- Creating a new dataset for ML training or evaluation
- Preparing existing raw data for model consumption
- Cleaning, deduplicating, or augmenting datasets
- Generating synthetic training examples via LLMs
- Splitting datasets into train/validation/test sets
- Formatting data for instruction tuning (Alpaca, ShareGPT, ChatML)
- Training or fine-tuning models with prepared datasets

## Iron Laws

1. **Split before touch** — Separate train/validation/test before ANY preprocessing. Data leakage through preprocessing is the #1 ML bug.
2. **Data card required** — Every dataset must document source, collection method, known biases, and usage restrictions.
3. **Version everything** — Datasets, labels, and preprocessing code must be versioned together for reproducibility.
4. **Class balance awareness** — Know your class distribution. Imbalanced datasets need explicit handling (oversampling, weighting, stratified splitting).
5. **Quality > quantity** — Noisy, biased, or leaked data is worse than less clean data.

## Workflow

### Phase 1: Define & Collect

**1.1 Define the objective**

Before collecting data, answer:
- What task will the model perform? (classification, generation, Q&A, reasoning)
- What are the input/output types?
- What is the target performance metric?
- What are the constraints? (privacy, licensing, latency, budget)

**1.2 Identify data sources**

| Source Type | Best For | Considerations |
|---|---|---|
| Existing public datasets | Baseline, benchmarking | Check license, verify quality |
| Web scraping | Domain-specific text | Legal review required, clean aggressively |
| Internal logs / databases | Production-aligned data | PII risk, access controls |
| Human annotation | High-precision labels | Expensive, needs guidelines |
| Synthetic generation | Augmentation, bootstrapping | Risk of model collapse, verify quality |

**1.3 Collect raw data**

```python
import pandas as pd

# Example: Load from multiple sources
sources = [
    pd.read_csv("source_a.csv"),
    pd.read_json("source_b.jsonl", lines=True),
    pd.read_parquet("source_c.parquet"),
]

raw = pd.concat(sources, ignore_index=True)
print(f"Collected {len(raw)} raw records")
print(f"Columns: {raw.columns.tolist()}")