# Example Feature Specs — Quick Reference

This directory contains ready-to-use `features.json` files for the six canonical dataset families. Copy one as the starting point for your `features.json` and customize the field names/types as needed.

## When to use each

| File | Family | When to use | Canonical source |
|---|---|---|---|
| `instruction-tuning.json` | Instruction-tuning (Alpaca-style) | Single-turn `(instruction, input, output)` triples for SFT | `tatsu-lab/alpaca` (52K rows) |
| `chat.json` | Chat / multi-turn dialogue | Multi-turn conversations as `messages: [{role, content}]` | `HuggingFaceH4/ultrachat_200k` (200K rows) |
| `preference-dpo.json` | Preference / DPO / RLHF | `(prompt, chosen, rejected)` pairs for DPO/ORPO/KTO training | `HuggingFaceH4/ultrafeedback_binarized` (61K train_prefs) |
| `pretraining.json` | Pretraining corpus (FineWeb-style) | `(text, id, url, ...)` documents with full provenance | `HuggingFaceFW/fineweb` (15T tokens) |
| `benchmark-mcq.json` | Benchmark — multiple-choice (MMLU-style) | `(question, choices, answer)` with `answer` as ClassLabel | `cais/mmlu` (57 subject configs) |
| `benchmark-qa.json` | Benchmark — extractive QA (SQuAD-style) | `(question, context, answers)` with span offsets | `rajpurkar/squad` (87K questions) |

## Schema details

For the full feature schema (Python `Features` definition, YAML `dataset_info.features` block, and one example row), see `references/schemas.md` in the skill root.

## How to use

### With `produce_dataset.py`

```bash
# 1. Copy the spec to your working directory
cp /home/z/my-project/skills/dataset-producer/assets/example_features/instruction-tuning.json \
   /home/z/my-project/download/my_dataset/features.json

# 2. (Optional) Edit features.json to add or remove fields

# 3. Build the parquet shards
python /home/z/my-project/skills/dataset-producer/scripts/produce_dataset.py \
  --input raw.jsonl \
  --features /home/z/my-project/download/my_dataset/features.json \
  --splits train:0.9,test:0.1 \
  --out /home/z/my-project/download/my_dataset/data/
```

### With `make_card.py`

The same `features.json` is reused by `make_card.py` to generate the YAML frontmatter:

```bash
python /home/z/my-project/skills/dataset-producer/scripts/make_card.py \
  --name "my-dataset" \
  --license cc-by-4.0 \
  --language en \
  --task text-generation \
  --features /home/z/my-project/download/my_dataset/features.json \
  --stats /home/z/my-project/download/my_dataset/stats.json \
  --auto-example \
  --out /home/z/my-project/download/my_dataset/README.md
```

## Customizing the schema

If none of the six canonical families fits, design a custom schema using the type vocabulary in `references/yaml-spec.md` (the types are `Value`, `Sequence`, `list` of structs, `struct`, `class_label`, `Image`, `Audio`).

### Common customizations

| You want to... | Edit |
|---|---|
| Add a `system` prompt field to instruction-tuning | Add `"system": {"_type": "Value", "dtype": "string"}` |
| Add per-row metadata (`id`, `source`, `date`) | Add three `Value("string")` fields |
| Add a 5-option MCQ instead of 4-option | Change `ClassLabel` `names` to `["A", "B", "C", "D", "E"]` |
| Add a tool-call field to chat | Add a `tool_calls` field as a `List` of structs (see `schemas.md` for an example) |
| Add judge metadata to DPO | Add `labelling_model`, `rationale` fields (see `schemas.md`) |
| Add `token_count` to pretraining | Add `Value("int64")` field |

## Format

All specs use the JSON form that `Features.to_dict()` produces:

```json
{
  "<field_name>": {
    "_type": "Value" | "ClassLabel" | "Sequence" | "List" | "struct",
    ...
  }
}
```

The `_parse_feature_spec()` function in `produce_dataset.py` accepts both this JSON form and the equivalent Python dict form. Both `_type: "Sequence"` and `_type: "List"` are recognized (HF rewrites `Sequence` to `List` in some code paths; we handle both).
