# Format Decision Guide — When to Use Which Dataset Format

> HuggingFace's official guidance (from `docs/hub/en/datasets-upload-guide-llm`): **prefer Parquet when possible**; JSON/JSONL or CSV are acceptable for smaller datasets; raw files work well for images/audio in smaller datasets; use WebDataset (`.tar`) for large media collections.
>
> This file gives you the decision matrix and the sharding patterns.

## TL;DR — Default decision tree

```
Is the dataset < 500 MB and one-shot (no sharding needed)?
├── YES → JSONL (human-readable, streams fine)
└── NO → Parquet (columnar, typed, compressed)

Is the dataset pretraining-scale (> 100 GB)?
├── YES → URL-manifest pattern (Dolma) — host data in object storage, repo holds urls/vX.txt
└── NO → Sharded Parquet, 1–5 GB per shard

Does the dataset contain images or audio?
├── < 100 files → embedded in Parquet (Image / Audio feature types)
├── < 10K files → WebDataset (.tar) with sidecar parquet metadata
└── > 10K files → WebDataset (.tar), partitioned
```

## Format decision matrix

| Format | When to use | Pros | Cons | Max practical size |
|---|---|---|---|---|
| **Parquet** (`.parquet`) | Default for anything that needs the Dataset Viewer, type safety, or compression. Best for ≥ a few MB up to TB-scale. | Columnar (read only needed columns); rich type system (lists, structs, ClassLabel, Image, Audio); 5–10× smaller than JSON; supports predicate pushdown via DuckDB/Polars; schema is self-describing; HF auto-converts other formats to parquet for the Viewer | Binary — not human-readable without a tool (pyarrow, DuckDB, pandas) | Up to 50 GB per file (HF recommendation); shard larger datasets |
| **JSONL** (`.jsonl` / `.jsonl.gz`) | Streaming pipelines, raw exports, datasets where each row is a complex nested object you want to eyeball | One JSON object per line → append-only, streamable, greppable; reads in any language; great for logs/dialogue trees | No type safety (mixed dtypes silently work); 5–10× larger than parquet; slow to read columns; no predicate pushdown | ~1 GB per file recommended; gzip-compressed OK up to ~5 GB |
| **CSV / TSV** (`.csv` / `.tsv`) | Small tabular data; quick prototypes; interop with spreadsheets | Trivially readable; opens in Excel; smallest overhead for narrow tables | No nesting (only scalars); no type info (everything is a string until parsed); no arrays; quotes/commas in data are a footgun | < 1 GB recommended |
| **Arrow** (`.arrow` / IPC) | Interop with the `datasets` cache; rarely uploaded directly | Zero-copy reads; in-memory speed; preserves Arrow types exactly | Larger than parquet on disk (no compression by default); poor Hub viewer support | Use parquet instead |
| **Raw text** (`.txt`) | Pretraining corpora where you want maximum tokenizer throughput | Simplest possible format; trivial to stream | No metadata, no IDs, no per-row fields | Combine with `.zst`/`.gz` for large corpora |
| **Compressed text** (`.zst`, `.gz`, `.bz2`) | Huge pretraining corpora (Dolma, RedPajama) | 3–5× compression; streamable with `zstandard`/`gzip` | Need to decompress to read; no random access | Petabyte-scale |
| **WebDataset** (`.tar` / `.tar.gz`) | Large media (image/audio/video) for streaming training | Sequential I/O → ideal for cloud training; one file per sample; pairs naturally with `.parquet` sidecar metadata | Not columnar; harder to query | 1–5 GB per tar shard recommended |
| **Single JSON** (`.json`) | Tiny datasets (< 1K rows) | Human-readable | Doesn't stream; slow to parse; no partial reads | Avoid for > 1K rows |

## Parquet — the recommended default

### Why parquet wins

1. **Columnar** — read only the columns you need (e.g., just `text` and `language` from a 15-column corpus). JSONL forces you to parse every row.
2. **Rich type system** — `list`, `struct`, `class_label`, `Image`, `Audio` are first-class. The Dataset Viewer renders dropdowns for `ClassLabel`, displays images for `Image`, plays audio for `Audio`.
3. **5–10× smaller than JSON** — parquet uses dictionary encoding, run-length encoding, and snappy/zstd compression by default.
4. **Self-describing schema** — the parquet file header contains the schema, so the loader doesn't need an external spec.
5. **Predicate pushdown** — DuckDB and Polars can push `WHERE` clauses into the parquet reader, skipping entire row groups. JSONL can't do this.
6. **HF auto-converts everything else to parquet** for the Dataset Viewer — so uploading native parquet yourself gives you control over shard boundaries and lets you declare the schema explicitly in YAML.

### Sharding pattern (mandatory naming convention)

```
<split>-<NNNNN>-of-<NNNNN>[-<hash>].parquet
```

- `<split>`: `train`, `test`, `validation`, or custom (`train_sft`, `train_prefs`).
- `<NNNNN>-of-<NNNNN>`: shard index zero-padded to 5 digits, total shard count zero-padded to 5 digits. Lets the loader infer the shard count from any one file name.
- `<hash>` (optional): 16-hex content hash added by `push_to_hub()` for cache-busting / content addressing. Drop it for hand-built shards.

**Examples:**
- `train-00000-of-00003.parquet` — 3-shard train split.
- `test-00000-of-00001.parquet` — single-shard test split.
- `train_sft-00000-of-00003-a3ecf92756993583.parquet` — UltraChat 200k style (content-hash suffix).

### Shard size guidance (from HF upload guide)

| Constraint | Value | Why |
|---|---|---|
| Per-file hard limit | 200 GB | LFS |
| Per-file recommended | < 50 GB | |
| Per-folder recommended | < 10,000 files | Git performance threshold |
| Per-repo soft cap (public) | 300 GB | Contact HF for larger |
| `viewer_row_size_mb` | 2 MB | Keep individual rows under ~2 MB so the Viewer can sample them |

### Sharding strategy by dataset size

| Dataset size | Sharding strategy |
|---|---|
| < 500 MB | Single shard: `train-00000-of-00001.parquet` |
| 500 MB – 5 GB | Single shard per split, or 2-3 shards if > 1 GB |
| 5 GB – 100 GB | 1–5 GB per shard, flat in `data/` directory |
| 100 GB – 1 TB | 1–5 GB per shard, partitioned by source/date in subdirectories |
| > 1 TB (pretraining-scale) | URL-manifest pattern (Dolma) — data lives in object storage, repo holds only `urls/vX.txt` + loader script |

### Multi-config sharding

Two valid patterns:

**A. One directory per config** (MMLU, GSM8K, FineWeb):
```
my_dataset/
├── README.md
├── data/
│   ├── main/
│   │   ├── train-00000-of-00001.parquet
│   │   └── test-00000-of-00001.parquet
│   └── socratic/
│       ├── train-00000-of-00001.parquet
│       └── test-00000-of-00001.parquet
```

**B. Flat with split name in file** (UltraChat 200k):
```
my_dataset/
├── README.md
└── data/
    ├── train_sft-00000-of-00003.parquet
    ├── train_sft-00001-of-00003.parquet
    ├── train_sft-00002-of-00003.parquet
    ├── test_sft-00000-of-00001.parquet
    ├── train_gen-00000-of-00003.parquet
    └── ...
```

Pattern A is cleaner when configs have **different schemas**. Pattern B is fine when configs share a schema but represent different **processing stages** (SFT vs generation).

### Image / Audio in parquet

For small image/audio datasets (< 100 files), embed them directly using `Image` / `Audio` feature types:

```python
from datasets import Dataset, Features, Value, Image, Audio

features = Features({
    "image":     Image(),
    "caption":   Value("string"),
    "audio":     Audio(sampling_rate=16000),
})

dataset = Dataset.from_dict({...}, features=features)
dataset.to_parquet("data/train-00000-of-00001.parquet")
```

Parquet stores images as bytes; the loader decodes them to PIL on read. Works fine up to ~10K images per shard. For larger media collections, use WebDataset.

## JSONL — the streaming alternative

### When JSONL is the right call

- **Streaming pipelines** where you append rows continuously (logs, real-time annotation).
- **Raw exports** where you want the original data preserved verbatim (OASST1 ships both parquet for the Viewer AND raw `.jsonl.gz` exports for researchers).
- **Eyeballing** — when you want to `head -n 5 data.jsonl | jq .` to inspect rows.
- **Cross-language interop** — JSONL is read by every language; parquet requires `pyarrow` or `duckdb`.

### When JSONL is the wrong call

- Datasets that need the Dataset Viewer to render dropdowns / images / audio (parquet only).
- Datasets > 1 GB (parquet is 5–10× smaller).
- Datasets where you query by column frequently (parquet predicate pushdown is much faster).

### Best practice: ship both

OASST1's pattern — clean parquet in `data/` for the Viewer + raw `.jsonl.gz` at the repo root for researchers — is the gold standard for transparent datasets:

```
my_dataset/
├── README.md
├── data/
│   ├── train-00000-of-00001.parquet
│   └── validation-00000-of-00001.parquet
└── raw/
    ├── 2024-01-15_messages.jsonl.gz
    └── 2024-01-15_trees.jsonl.gz
```

The YAML `configs` block only points at `data/`; the `raw/` files are documentation, not loader targets.

## URL-manifest pattern (Dolma)

For pretraining-scale corpora where even sharded parquet is too big to host in the repo:

```
my_corpus/
├── README.md
├── .gitattributes
├── LICENSE.md
├── loader.py                          # custom loader script
└── urls/
    ├── v1.txt                         # one URL per line, pointing to zstd-compressed jsonl shards in S3
    ├── v1_5.txt
    └── v1_7.txt                       # current default version
```

YAML:
```yaml
viewer: false      # the Viewer can't process petabyte-scale data
```

Users fetch shards in parallel:
```bash
aria2c -j 16 -i urls/v1_7.txt
```

Use this pattern only when the dataset is genuinely pretraining-scale (> 100 GB). For everything else, host the parquet in the repo.

## WebDataset — for large media

For image/audio/video datasets with > 10K samples, use WebDataset (`.tar` shards) with a sidecar parquet for metadata:

```
my_audio_dataset/
├── README.md
├── data/
│   ├── shards/
│   │   ├── shard-000000.tar          # 1–5 GB each, contains .wav + .json metadata pairs
│   │   ├── shard-000001.tar
│   │   └── ...
│   └── metadata.parquet              # sidecar: id, transcript, speaker_id, shard_idx, offset
```

Each `.tar` shard contains paired files: `000001.wav`, `000001.json`, `000002.wav`, `000002.json`, …

WebDataset is sequential I/O — ideal for cloud training (no random reads). Pair with a sidecar parquet for filtering and querying.

## When the format isn't your choice

If your dataset is already in CSV/JSON, you don't have to convert it yourself — the Dataset Viewer's `refs/convert/parquet` branch auto-converts every supported dataset to parquet behind the scenes. The conversion endpoint is `https://datasets-server.huggingface.co/parquet?dataset=<id>`.

That said, **uploading native parquet yourself is still preferred** because:

1. You control shard boundaries (HF auto-conversion makes 1-shard-per-split; you may want 3-shard train).
2. You can declare the schema explicitly in YAML (auto-conversion infers it; sometimes wrong — e.g., ClassLabel becomes `int64`).
3. No conversion lag (auto-conversion takes 5–30 minutes after upload).
4. You can use `Image`/`Audio` feature types (auto-conversion leaves them as `binary`).

## Special cases

### Multiple-choice with variable choices per row

ARC, OpenBookQA have variable number of choices. Use `sequence: string` (not `class_label`):

```yaml
- name: choices
  sequence: string
- name: answer
  dtype: string              # "A" / "B" / ... / or the literal text
```

Or use `ClassLabel` with the max number of choices and pad with empty strings:

```yaml
- name: choices
  sequence: string           # always length N (pad with "")
- name: answer
  dtype:
    class_label:
      names:
        '0': A
        '1': B
        '2': C
        '3': D
        '4': E
```

### Nested annotations (OASST-style)

For richly-annotated datasets with per-message toxicity scores, labels, emojis, etc., use `struct:` and `list:`:

```yaml
- name: detoxify
  struct:
    - name: toxicity
      dtype: float64
    - name: severe_toxicity
      dtype: float64
- name: labels
  sequence:
    - name: name
      dtype: string
    - name: value
      dtype: float64
    - name: count
      dtype: int32
```

### Translations

For parallel-text datasets (machine translation), use `Translation`:

```python
from datasets import Translation
features = Features({"translation": Translation(languages=["en", "fr"])})
```

In YAML:
```yaml
- name: translation
  dtype:
    translation:
      languages:
        - en
        - fr
```

Each row: `{"translation": {"en": "...", "fr": "..."}}`.

## Final rule of thumb

**Default to parquet.** Ship JSONL alongside only for transparency. Use WebDataset for large media. Use URL-manifest only for pretraining-scale. Everything else is parquet.
