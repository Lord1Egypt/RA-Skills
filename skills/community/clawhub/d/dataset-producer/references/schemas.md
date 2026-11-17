# Feature Schemas for the Six Canonical Dataset Families (plus the OASST1 bonus)

> Use this file to pick the right schema for your dataset. Each family below shows the Python `datasets.Features` definition, the corresponding YAML `dataset_info.features` block, and one example row. The Python and YAML must match exactly — the YAML is what the HF loader reads, the Python object is what you validate against at build time.
>
> This file documents **six canonical families** (instruction-tuning, chat, preference/DPO, pretraining, benchmark-MCQ, benchmark-QA) plus the **OASST1 bonus** for richly-annotated dialogue. Most new datasets use one of the six canonical families.

## Table of Contents

- [How to read these schemas](#how-to-read-these-schemas)
- [1. Instruction-tuning (Alpaca-style)](#1-instruction-tuning-alpaca-style)
- [2. Chat / multi-turn dialogue (UltraChat-style)](#2-chat--multi-turn-dialogue-ultrachat-style)
- [3. Preference / DPO / RLHF (UltraFeedback-style)](#3-preference--dpo--rlhf-ultrafeedback-style)
- [4. Pretraining corpus (FineWeb-style)](#4-pretraining-corpus-fineweb-style)
- [5. Benchmark — multiple-choice (MMLU-style)](#5-benchmark--multiple-choice-mmlu-style)
- [6. Benchmark — extractive QA (SQuAD-style)](#6-benchmark--extractive-qa-squad-style)
- [7. Bonus: richly-annotated chat (OASST1-style)](#7-bonus-richly-annotated-chat-oasst1-style)
- [Choosing between families](#choosing-between-families)
- [Type vocabulary quick reference](#type-vocabulary-quick-reference)

---

## How to read these schemas

Each schema is shown in three forms:

1. **Python `Features`** — for build-time validation. Pass to `Dataset.from_dict(data, features=features)` or `Dataset.from_generator(gen, features=features)`.
2. **YAML `dataset_info.features`** — for the README.md frontmatter. Copied verbatim under the `dataset_info:` block.
3. **Example row** — a single concrete JSON object. Use this in the README's `### Data Instances` section.

When in doubt, mirror the canonical source dataset's schema exactly. Downstream tools (TRL, OpenAI client, Anthropic client) expect these shapes.

---

## 1. Instruction-tuning (Alpaca-style)

**Canonical source**: `tatsu-lab/alpaca` (52K rows).

**When to use**: single-turn task → response. The simplest SFT format. Each row is one (instruction, optional input, expected output) triple.

**When NOT to use**: multi-turn dialogue → use the chat schema. Preference data (chosen vs rejected) → use the DPO schema.

### Python Features

```python
from datasets import Features, Value

features = Features({
    "instruction": Value("string"),  # the task description
    "input":       Value("string"),  # optional context; empty string if none
    "output":      Value("string"),  # the demonstration response
    "text":        Value("string"),  # optional: pre-formatted prompt+response
    # Optional enrichment:
    "system":      Value("string"),  # system prompt, if you use one
    "id":          Value("string"),  # stable row ID for dedup/tracing
    "source":      Value("string"),  # which seed task / generator produced this row
})
```

Drop `text` if you don't pre-format — most modern trainers (TRL `SFTTrainer`) accept `(instruction, input, output)` and apply the chat template at train time.

### YAML

```yaml
dataset_info:
  features:
    - name: instruction
      dtype: string
    - name: input
      dtype: string
    - name: output
      dtype: string
    - name: text
      dtype: string
    - name: system
      dtype: string
    - name: id
      dtype: string
    - name: source
      dtype: string
  splits:
    - name: train
      num_examples: 52002
```

### Example row

```json
{
  "instruction": "Create a classification task by clustering the given list of items.",
  "input": "Apples, oranges, bananas, strawberries, pineapples",
  "output": "Class 1: Apples, Oranges\nClass 2: Bananas, Strawberries\nClass 3: Pineapples",
  "text": "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.\n\n### Instruction:\nCreate a classification task by clustering the given list of items.\n\n### Input:\nApples, oranges, bananas, strawberries, pineapples\n\n### Response:\nClass 1: Apples, Oranges\nClass 2: Bananas, Strawberries\nClass 3: Pineapples",
  "system": "",
  "id": "alpaca_00001",
  "source": "self-instruct"
}
```

### Variants

- **Dolly 15K** — adds `category` (closed-class task type) and `context` instead of `input`.
- **OpenOrca / FLAN** — adds `question_id`, `dataset` (which FLAN task), `system_prompt`.
- **WizardLM** — adds `conversation` field with the full evol-instruct trace.

---

## 2. Chat / multi-turn dialogue (UltraChat-style)

**Canonical source**: `HuggingFaceH4/ultrachat_200k` (1.4M → 200K filtered ChatGPT dialogues).

**When to use**: multi-turn dialogue. Each row is one conversation: a list of `{role, content}` messages.

**When NOT to use**: single-turn → instruction-tuning is simpler. Preference data → DPO schema.

### Python Features

```python
from datasets import Features, Value, Sequence

features = Features({
    "prompt":     Value("string"),  # the initial user message (also messages[0].content)
    "prompt_id":  Value("string"),  # sha256 of prompt — for dedup and traceability
    "messages":   Sequence({
        "role":    Value("string"),    # "system" | "user" | "assistant" | "tool"
        "content": Value("string"),
    }),
})
```

For tool-use conversations, extend each message with `tool_calls`:

```python
features = Features({
    "messages": Sequence({
        "role":    Value("string"),
        "content": Value("string"),
        "tool_calls": Sequence({             # only present on assistant messages that call tools
            "id":   Value("string"),
            "type": Value("string"),         # "function"
            "function": {
                "name":      Value("string"),
                "arguments": Value("string"),  # JSON string; keys vary per tool
            },
        }),
    }),
})
```

### YAML

```yaml
dataset_info:
  features:
    - name: prompt
      dtype: string
    - name: prompt_id
      dtype: string
    - name: messages
      list:
        - name: role
          dtype: string
        - name: content
          dtype: string
  splits:
    - name: train_sft
      num_examples: 207865
    - name: test_sft
      num_examples: 23110
```

### Example row

```json
{
  "prompt": "Create a fully-developed protagonist who is challenged to survive within a dystopian society...",
  "prompt_id": "d938b65dfe31f05f80eb8572964c6673eddbd68eff3db6bd234d7f1e3b86c2af",
  "messages": [
    {"role": "user", "content": "Create a fully-developed protagonist..."},
    {"role": "assistant", "content": "Name: Ava\n\nAva was just 16 years old..."},
    {"role": "user", "content": "Wow, Ava's story is so intense! Can you provide me with more details."},
    {"role": "assistant", "content": "Certainly! ..."}
  ]
}
```

### Conventions

- `messages` is the **canonical chat format** adopted by TRL, OpenAI, Anthropic, and the OpenAI chat completions API. `role` ∈ `{system, user, assistant, tool}`.
- `prompt` + `prompt_id` are precomputed so SFT and generation splits can be aligned. `prompt_id = sha256(prompt).hexdigest()`.
- Convention: alternate `user`/`assistant` starting with `user`. Insert a `system` message at index 0 if needed.
- For tool use, add `tool_calls` on assistant messages and `name` on tool-role messages.

---

## 3. Preference / DPO / RLHF (UltraFeedback-style)

**Canonical source**: `HuggingFaceH4/ultrafeedback_binarized` (6 splits: `{train,test}_{sft,prefs,gen}`).

**When to use**: preference learning. Each row is one prompt + a chosen (preferred) response + a rejected (dispreferred) response. Trains DPO, ORPO, KTO, and other preference-learning algorithms.

**When NOT to use**: if you only have one response per prompt → use chat or instruction-tuning.

### Python Features (message-list form — preferred by TRL)

```python
from datasets import Features, Value, Sequence

features = Features({
    "prompt":         Value("string"),
    "prompt_id":      Value("string"),
    "chosen":         Sequence({                 # the preferred trajectory
        "role":    Value("string"),
        "content": Value("string"),
    }),
    "rejected":       Sequence({                 # the dispreferred trajectory
        "role":    Value("string"),
        "content": Value("string"),
    }),
    "messages":       Sequence({                 # the chosen trajectory (for SFT co-training)
        "role":    Value("string"),
        "content": Value("string"),
    }),
    "score_chosen":   Value("float64"),          # reward model score of chosen
    "score_rejected": Value("float64"),          # reward model score of rejected
})
```

### Python Features (flat-string form — simpler, older trainers)

```python
features = Features({
    "system":   Value("string"),   # optional system prompt
    "input":    Value("string"),   # the prompt
    "chosen":   Value("string"),   # chosen response (string, not message list)
    "rejected": Value("string"),   # rejected response (string)
    # Optional judge metadata:
    "chosen_score":         Value("float64"),
    "rejected_score":       Value("float64"),
    "status":               Value("string"),   # "chosen" | "rejected" | "tie"
    "rating":               Sequence(Value("float64")),   # judge ratings per generation
    "rationale":            Value("string"),   # judge's natural-language rationale
    "labelling_model":      Value("string"),   # which LLM judged this pair
    "labelling_prompt":     Sequence({         # the judge prompt, as a message list
        "role":    Value("string"),
        "content": Value("string"),
    }),
    "raw_labelling_response": Value("string"),
    # Contamination flag (UltraFeedback Binarized adds this after community flagged TruthfulQA leakage):
    "in_gsm8k_train":        Value("bool"),
})
```

### YAML (message-list form)

```yaml
dataset_info:
  features:
    - name: prompt
      dtype: string
    - name: prompt_id
      dtype: string
    - name: chosen
      list:
        - name: content
          dtype: string
        - name: role
          dtype: string
    - name: rejected
      list:
        - name: content
          dtype: string
        - name: role
          dtype: string
    - name: messages
      list:
        - name: content
          dtype: string
        - name: role
          dtype: string
    - name: score_chosen
      dtype: float64
    - name: score_rejected
      dtype: float64
  splits:
    - name: train_prefs
      num_examples: 61135
    - name: test_prefs
      num_examples: 2000
```

### Example row

```json
{
  "prompt": "What is the capital of France?",
  "prompt_id": "abc123def456...",
  "chosen":   [{"role": "user", "content": "What is the capital of France?"},
               {"role": "assistant", "content": "The capital of France is Paris."}],
  "rejected": [{"role": "user", "content": "What is the capital of France?"},
               {"role": "assistant", "content": "I think it might be London, but I'm not sure."}],
  "messages": [{"role": "user", "content": "What is the capital of France?"},
               {"role": "assistant", "content": "The capital of France is Paris."}],
  "score_chosen":   8.5,
  "score_rejected": 2.1
}
```

### Conventions

- The **message-list form** supports multi-turn preferences; the flat-string form does not. Prefer message-list for new datasets.
- `chosen` and `rejected` should share the same prompt prefix; only the final assistant turn differs. Otherwise the comparison is unfair.
- `score_chosen > score_rejected` is a hard invariant — validate it before publishing.
- For KTO (Kahneman-Tversky Optimization), you don't need pairs — just `{prompt, completion, label: bool}` (label=true if the completion was desirable). Use a custom schema for KTO.

---

## 4. Pretraining corpus (FineWeb-style)

**Canonical source**: `HuggingFaceFW/fineweb` (15T tokens; multi-config; sharded parquet partitioned by CommonCrawl dump).

**When to use**: base-model pretraining. Each row is one document with full provenance.

**When NOT to use**: instruction-following → instruction-tuning. Dialogue → chat. If you only have text and don't care about provenance, drop the optional fields — but provenance is strongly recommended for any dataset someone might pretrain on.

### Python Features

```python
from datasets import Features, Value

features = Features({
    "text":            Value("string"),  # the main document content
    "id":              Value("string"),  # globally unique, e.g. "urn:uuid:..." or sha256
    "dump":            Value("string"),  # which source dump, e.g. "CC-MAIN-2021-43"
    "url":             Value("string"),  # source URL
    "date":            Value("string"),  # crawl timestamp ISO-8601
    "file_path":       Value("string"),  # path of the source WARC/file
    "language":        Value("string"),  # ISO 639-1
    "language_score":  Value("float64"), # fastText lang-ID confidence, 0.0–1.0
    "token_count":     Value("int64"),   # precomputed token count for sampling budgets
})
```

### YAML

```yaml
dataset_info:
  features:
    - name: text
      dtype: string
    - name: id
      dtype: string
    - name: dump
      dtype: string
    - name: url
      dtype: string
    - name: date
      dtype: string
    - name: file_path
      dtype: string
    - name: language
      dtype: string
    - name: language_score
      dtype: float64
    - name: token_count
      dtype: int64
  splits:
    - name: train
      num_examples: 15000000000  # ~15B docs
```

### Example row

```json
{
  "text": "This is basically a peanut flavoured cream thickened with egg yolks and then set into a ramekin on top of some jam...",
  "id": "urn:uuid:e5a3e79a-13d4-4147-a26e-167536fcac5d",
  "dump": "CC-MAIN-2021-43",
  "url": "http://allrecipes.co.uk/recipe/24758/peanut-butter-and-jam-creme-brulee.aspx",
  "date": "2021-10-15T21:20:12Z",
  "file_path": "s3://commoncrawl/crawl-data/CC-MAIN-2021-43/segments/.../CC-MAIN-...00600.warc.gz",
  "language": "en",
  "language_score": 0.948729,
  "token_count": 69
}
```

### Variants

- **Dolma** (3T tokens, mixed sources) — stored as `.jsonl.zst` shards hosted externally; repo holds only `urls/vX.txt` + loader script. YAML sets `viewer: false`.
- **RedPajama** — similar to FineWeb; per-source partitioning.
- **The Stack v2** (code) — adds `language` (programming language), `size_bytes`, `extension`, `is_vendor`.

### Pretraining-specific tips

- Always dedup: exact + fuzzy (MinHash LSH). FineWeb and Dolma both do this; publishing a dedup'd corpus is mandatory for pretraining quality.
- Set `viewer: false` in YAML for >1B-row corpora — the Dataset Viewer can't pre-process petabyte-scale data.
- Per-source provenance tables in the README are standard (FineWeb and Dolma both publish them).
- Consider publishing a `sample-<N>BT` config alongside the full corpus so users can prototype cheaply.

---

## 5. Benchmark — multiple-choice (MMLU-style)

**Canonical source**: `cais/mmlu` (57 subject configs + an `all` aggregator; 4-way MCQ).

**When to use**: multiple-choice evaluation. Each row is one question + N options + the correct answer index.

**When NOT to use**: free-form QA → use the SQuAD-style schema. Generation tasks → instruction-tuning.

### Python Features

```python
from datasets import Features, Value, ClassLabel, Sequence

features = Features({
    "question":  Value("string"),
    "subject":   Value("string"),                 # subject slug, e.g. "anatomy"
    "choices":   Sequence(Value("string")),        # exactly N options (4 for MMLU)
    "answer":    ClassLabel(names=["A", "B", "C", "D"]),  # stored as int; ClassLabel int2str() → "A".."D"
})
```

For variable-arity MCQ (ARC, OpenBookQA), `choices` is still a `Sequence(Value("string"))` but the length varies per row, and `ClassLabel(names=...)` must cover the max length.

### YAML (multi-config form — one config_name per subject)

```yaml
dataset_info:
  - config_name: anatomy
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
        num_examples: 135
      - name: validation
        num_examples: 14
      - name: dev            # 5-shot examples for few-shot eval
        num_examples: 5
  - config_name: all
    features: ...            # same feature block
    splits:
      - name: test
        num_examples: 14042
```

### YAML (single-config form — for one-subject benchmarks)

```yaml
dataset_info:
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
      num_examples: 1000
```

### Example row

```json
{
  "question": "Which of the following is a primary lesion?",
  "subject": "anatomy",
  "choices": ["Macule", "Papule", "Nodule", "All of the above"],
  "answer": 3
}
```

(`answer` is stored as int 3; `ClassLabel.int2str(3)` returns `"D"`.)

### Conventions

- `answer` is a `ClassLabel`, not a `string`. This makes the Dataset Viewer render a dropdown and lets `dataset["answer"]` return ints directly.
- Provide a `dev` split (5-shot examples) for few-shot evaluation, separate from `validation` (hyperparameter tuning) and `test` (final score).
- For multi-config benchmarks, mirror MMLU's pattern: one config per subject + an `all` aggregator.

### BharatGen BhashaBench pattern (multilingual MCQ)

For multilingual benchmarks, mirror BharatGen's BhashaBench-Multi: **one config per domain** + **one split per language** (split name = English language name).

```yaml
configs:
  - config_name: BBA          # BhashaBench Ayur
    data_files:
      - split: english
        path: bhashabench_ayur/en.parquet
      - split: hindi
        path: bhashabench_ayur/hi.parquet
      # ... one per language
```

This lets users `load_dataset("repo", "BBA", split="hindi")` to get the Hindi Ayurveda questions directly.

---

## 6. Benchmark — extractive QA (SQuAD-style)

**Canonical source**: `rajpurkar/squad` / `rajpurkar/squad_v2`.

**When to use**: extractive QA — given a context paragraph and a question, mark the answer span(s) in the context.

### Python Features

```python
from datasets import Features, Value, Sequence

features = Features({
    "id":            Value("string"),
    "title":         Value("string"),
    "context":       Value("string"),
    "question":      Value("string"),
    "answers": Sequence({
        "text":         Sequence(Value("string")),   # one or more acceptable answer strings
        "answer_start": Sequence(Value("int32")),     # char offsets into context
    }),
})
```

### YAML

```yaml
dataset_info:
  features:
    - name: id
      dtype: string
    - name: title
      dtype: string
    - name: context
      dtype: string
    - name: question
      dtype: string
    - name: answers
      sequence:
        - name: text
          dtype: string
        - name: answer_start
          dtype: int32
```

### Example row

```json
{
  "id": "5733be084776f41900661182",
  "title": "University_of_Notre_Dame",
  "context": "Architecturally, the school has a Catholic character. Atop the Main Building's gold dome...",
  "question": "To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?",
  "answers": {
    "text": ["Saint Bernadette Soubirous"],
    "answer_start": [515]
  }
}
```

For **unanswerable questions** (SQuAD v2), set `answers: {text: [], answer_start: []}` and add `is_impossible: true` (bool).

---

## 7. Bonus: richly-annotated chat (OASST1-style)

**Canonical source**: `OpenAssistant/oasst1`.

**When to use**: when every message carries crowd-sourced quality annotations (toxicity scores, spam flags, emojis, labels). Rare for new datasets — usually you'll use the simpler chat schema.

### Python Features (truncated — see OASST1 README for the full schema)

```python
features = Features({
    "message_id":      Value("string"),    # UUID
    "parent_id":       Value("string"),    # UUID of parent message (null for roots)
    "user_id":         Value("string"),    # hashed user ID
    "created_date":    Value("string"),
    "text":            Value("string"),
    "role":            Value("string"),    # "prompter" | "assistant"
    "lang":            Value("string"),
    "review_count":    Value("int32"),
    "review_result":   Value("bool"),      # spam-or-not overall
    "deleted":         Value("bool"),
    "rank":            Value("int32"),
    "synthetic":       Value("bool"),
    "model_name":      Value("string"),
    "detoxify": {                          # 7-axis toxicity scores
        "toxicity":          Value("float64"),
        "severe_toxicity":   Value("float64"),
        "obscene":           Value("float64"),
        "identity_attack":   Value("float64"),
        "insult":            Value("float64"),
        "threat":            Value("float64"),
        "sexual_explicit":   Value("float64"),
    },
    "message_tree_id": Value("string"),
    "tree_state":      Value("string"),    # "ready_for_export" | "aborted_low_grade" | ...
    "emojis":          Sequence({
        "name":  Value("string"),
        "count": Value("int32"),
    }),
    "labels":          Sequence({
        "name":  Value("string"),          # "spam" | "quality" | "toxicity" | "humor" | ...
        "value": Value("float64"),
        "count": Value("int32"),
    }),
})
```

Reach for this only when you have rich per-message annotations. Otherwise, the simple chat schema (#2) is easier to consume.

---

## Choosing between families

| If your data is… | Use family | Why |
|---|---|---|
| Single (task, response) pairs | Instruction-tuning | Simplest; TRL `SFTTrainer` reads it directly |
| Multi-turn conversations | Chat | The `messages` schema is the OpenAI/Anthropic/TRL standard |
| (prompt, chosen, rejected) triples | Preference (DPO) | Message-list form supports multi-turn preferences |
| A pile of text documents | Pretraining | Add provenance fields; always dedup |
| Q + 4 options + correct letter | Benchmark MCQ | `ClassLabel` makes the Viewer render dropdowns |
| Context + question + answer span | Benchmark QA | SQuAD-style; supports multiple acceptable answers |
| Richly-annotated dialogue (toxicity, spam, labels) | OASST-style | When you need per-message quality filtering |

If none fit, design a custom schema using the type vocabulary below.

---

## Type vocabulary quick reference

The `dtype:` field in YAML and the `Value(...)` constructor in Python accept these types:

| YAML | Python | Meaning |
|---|---|---|
| `dtype: string` | `Value("string")` | UTF-8 string |
| `dtype: int32` / `int64` | `Value("int32")` / `Value("int64")` | Signed integer |
| `dtype: uint32` / `uint64` | `Value("uint32")` / `Value("uint64")` | Unsigned integer |
| `dtype: float32` / `float64` | `Value("float32")` / `Value("float64")` | IEEE float |
| `dtype: bool` | `Value("bool")` | Boolean |
| `dtype: binary` | `Value("binary")` | Bytes |
| `dtype: timestamp[ms]` | `Value("timestamp[ms]")` | Timestamp (also `s`, `us`, `ns`) |
| `sequence: <dtype>` | `Sequence(Value(...))` | List of scalars |
| `list:` + nested `- name:` blocks | `Sequence({...})` | List of structs |
| `struct:` + nested `- name:` blocks | `{...}` (dict of features) | Nested struct |
| `dtype: class_label:` + `names:` | `ClassLabel(names=[...])` | Categorical (stored as int, mapped to string) |
| `_type: Image` | `Image()` | PIL image |
| `_type: Audio` + `sampling_rate:` | `Audio(sampling_rate=...)` | Audio array + sample rate |
| `_type: Video` | `Video()` | Video frames |
| `array2d:` / `array3d:` + `shape:` + `dtype:` | `Array2D` / `Array3D` | Fixed-shape arrays (e.g. images, spectrograms) |
| `translation:` | `Translation()` | Pair of strings (e.g. `{"en": ..., "fr": ...}`) |

For nested types in YAML, use `struct:` for dicts and `list:` for lists of structs. Example:

```yaml
- name: detoxify
  struct:
    - name: toxicity
      dtype: float64
    - name: severe_toxicity
      dtype: float64

- name: emojis
  sequence:
    - name: name
      dtype: string
    - name: count
      dtype: int32
```

When unsure, mirror a real dataset's schema from `huggingface.co/datasets/<id>/blob/main/README.md`.
