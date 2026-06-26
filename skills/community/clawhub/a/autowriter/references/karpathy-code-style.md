# Karpathy Code Style → Writing Style

## Code Characteristics and Writing Mappings

### 1. One File Does Everything

train.py: GPT model definition, optimizer, training loop, all in one file.

**→ Writing: One article, one core idea. Subsequent iterations only fix locally, never rewrite everything (matches autoresearch only modifying train.py).**

### 2. Direct Variable Names

Not `apply_pre_norm_layer_normalization` — just `norm`.

**→ Writing: Use technical terms directly when context is clear, no need to define every time. Readers aren't stupid.**

### 3. Minimal Comments, But Each One Counts

```python
# varunneal's FA3 is Hopper only, use kernels-community on non-Hopper GPUs
```

This kind of comment explains "why this choice," not "what this code does."

**→ Writing: Less "this function does X," more "why X instead of Y." The evaluation function's "actionability" dimension detects this.**

### 4. Centralized Constants

```python
TIME_BUDGET = 300  # 5 minutes
MAX_SEQ_LEN = 2048
```

**→ Writing: Core parameters/numbers defined clearly on first use, then used directly. `--depth` is the centralized parameter management for writing.**

### 5. No Fear of Exposing Internals

autoresearch's program.md is public — including all instructions given to the AI agent.

**→ Writing: Draft log fully public, writing process transparent. No hiding.**

### 6. dataclass Config

```python
@dataclass
class GPTConfig:
    sequence_len: int = 2048
    vocab_size: int = 32768
```

Clean, zero boilerplate.

**→ Writing: The `--depth` knob table uses a table format, parameters at a glance. The evaluation function uses a table, dimensions and weights at a glance.**

## Evaluation Function Code Style Signals

| Code Behavior | Corresponding Evaluation Dimension | Detection Point |
|---------------|-----------------------------------|-----------------|
| One file does everything | Information density | Are there paragraphs unrelated to the core idea? |
| Short variable names | Conciseness | Are there removable paragraphs that don't affect the article? |
| Few but valuable comments | Information density | Does every sentence carry new information? |
| No fear of exposing internals | Failure showcase | Does it include "what didn't work"? |
| Fixed constants | Actionability | Can readers act immediately after reading? |
| results.tsv records failures | Failure showcase | Does draft log record all iterations? |

## Ultimate Principle

Karpathy's code and writing share one trait: **respect the reader's intelligence and time.**

This skill's evaluation function quantifies that principle: information density measures "don't waste time," actionability measures "respect intelligence," conciseness measures "no filler."
