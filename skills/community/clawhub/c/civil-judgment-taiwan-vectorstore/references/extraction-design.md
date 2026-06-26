# Extraction Algorithm Design

> This file documents the design rationale and implementation details of the three
> extraction functions in `scripts/ingest.py`. Read this when you want to understand
> or modify the extraction rules.
>
> For metadata schema, canonicalization rules, and chunking parameters, see
> [internals.md](internals.md).

---

## Shared preprocessing: limiting to the court's own reasoning section

All three extraction functions operate on a **pre-filtered slice of the full text**,
not the entire judgment. The script first looks for the start of the court's own
reasoning section using the following headers (ordinal prefixes like「三、」are
also matched):

| Header | Notes |
|--------|-------|
| `本院之判斷` | Most common |
| `得心證之理由` | |
| `兩造爭執事項` | |
| `經查：` | |
| `茲分述如下：` | |

Only the text **from the matched header onwards** is passed to the extraction
functions. This avoids extracting from the parties' pleadings or procedural history,
which would produce noisy false positives.

**Exception**: judgments from 最高法院 always use the full text, because Supreme
Court judgments do not follow the standard header structure.

---

## Shared preprocessing: sentence splitting

All three functions split text into sentences using a character-by-character scan on
the Chinese full-stop「。」:

```python
for ch in text:
    current += ch
    if ch == "。":
        sentences.append(current.strip())
        current = ""
```

This preserves the「。」at the end of each sentence (rather than discarding it via
`split("。")`), which keeps sentence boundaries intact when sentences are later
joined back together.

---

## Shared noise filters

Applied per-sentence before any extraction logic:

| Filter | Condition | Rationale |
|--------|-----------|-----------|
| Party assertion | Sentence ends with `等語` / `等語。` / `等語，` | These are quotations of the parties' arguments, not the court's own findings |
| Prior court citation | Sentence starts with `原審以` / `原審認` / `原審為` | These repeat a lower court's view, not the current court's reasoning |

---

## `extract_reasoning_snippets` — Subsumption reasoning (涵攝推理)

**Goal**: capture the logical moment where the court applies a norm to the facts and
derives a legal conclusion (大前提 → 小前提 → 涵攝).

### Cue words

```python
REASONING_CUE_PATTERNS = [
    "是故", "因此", "準此", "可見", "由此可見",
    "即應", "爰依", "自應", "從而", "甚是",
    "茲因", "是則", "應認", "所以", "顯見", "顯然", "必然",
]
```

These are conjunctive or inferential connectives that signal the conclusion step of a
syllogism. The scan is a plain substring match — the first matching cue in the list
wins, and its string value is stored in the `cue` field for downstream analysis.

### Context window

```
[i-1]  ← fact-finding sentence (小前提)
[i]    ← cue sentence (涵攝 conclusion)  ← trigger
[i+1]  ← legal-effect sentence
```

Taking one sentence before and one after avoids truncating the reasoning mid-thought.
Both neighbour sentences are also passed through the noise filters before inclusion.

### Output

```json
{"cue": "從而", "snippet": "查原告主張...屬實。從而，被告應負損害賠償責任。依民法第184條...。"}
```

Maximum 30 snippets per document (`max_snippets=30`). Deduplication uses
`(cue, snippet[:150])` as a key.

---

## `extract_norm_snippets` — Legal norm citations with context (法條引用片段)

**Goal**: capture sentences that cite specific legal norms, together with enough
surrounding context to understand how the norm is applied.

### Norm detection

Norms are detected by `extract_norms()` using regex patterns, for example:

```python
re.compile(r"(?:民法|民事訴訟法|土地法|...)[^。\n]{0,60}?第\s*\d+\s*條(?:之\s*\d+)?")
re.compile(r"釋字第\s*\d+\s*號")
re.compile(r"最高法院\s*\d+\s*年度[^\n。]{0,20}?字第\s*\d+\s*號")
```

### Expansion rules (backward and forward)

A sentence containing a norm citation is expanded in two cases:

| Condition | Expansion |
|-----------|-----------|
| Sentence ends with `定有明文` or contains `判決意旨參照` / `判決參照` | Expand **backwards** by 1 sentence (to include the applied-fact context) |
| Sentence ends with `定有明文` AND next sentence starts with `又` | Also expand **forwards** by 1 sentence (the「又」clause continues the same norm block) |

These rules prevent snippets from being pure statute text with no applied-fact context.

### Additional exclusions

- Sentences starting with `原審以/原審認/原審為` are excluded (prior court citations).
- Sentences ending with `等語` are excluded (party assertions).

### Output

List of strings. Maximum 40 snippets per document. Deduplication on full snippet text.

---

## `extract_fact_reason_snippets` — Key fact-finding paragraphs (事實認定片段)

**Goal**: capture sentences where the court affirmatively states its factual findings,
signalled by the opening pattern「查/經查/惟查」.

These openings are a strong convention in Taiwan civil judgments:

| Opening | Typical usage |
|---------|---------------|
| `查` | Standard fact-finding opener |
| `經查` | "Upon examination" — evidence-based finding |
| `惟查` | "However, upon examination" — counter-finding |

### Context window

```
[i]    ← 查/經查/惟查 sentence  ← trigger
[i+1]  ← continuation or consequence
...up to window=2 sentences after
```

The window is wider than `extract_reasoning_snippets` (2 vs 1) because fact-finding
paragraphs tend to run longer before the conclusion.

### Output

List of strings. Maximum 60 snippets per document. Deduplication on full snippet text.

---

## Storage

All three extraction results are stored in the **doc-level Qdrant payload** (not in
chunk points):

| Field | Source function | Type |
|-------|----------------|------|
| `reasoning_snippets` | `extract_reasoning_snippets` | `List[{"cue": str, "snippet": str}]` |
| `norms_reasoning_snippets` | `extract_norm_snippets` | `List[str]` |
| `fact_reason_snippets` | `extract_fact_reason_snippets` | `List[str]` |
| `cited_norms` | `extract_norms` | `List[str]` |

Storing at doc level (rather than creating separate chunk points) keeps the pipeline
simple and avoids a third collection, at the cost of larger per-doc payloads.
