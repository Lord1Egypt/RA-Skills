# Audit Heuristics

Use these heuristics when the hard part is not summarization, but evidence discipline.

## Support Levels

### Direct Evidence

Use when the source explicitly states the claim or directly records the fact.

Good phrasing:
- `资料直接写明了这一点。`
- `这属于直接证据，不需要额外推断。`

### Corroborated Evidence

Use when several independent or differently-situated sources point to the same conclusion.

Good phrasing:
- `多份资料共同支持这个判断。`
- `这不是单一来源的说法。`

### Inference

Use when the conclusion is reasonable, but the sources do not state it outright.

Good phrasing:
- `这个结论更像推断。`
- `资料提供了信号，但没有直接下这个结论。`

### Assumption

Use when the claim is plausible, but the current material does not really support it.

Good phrasing:
- `这一步还是假设。`
- `目前没有足够证据把它当成结论。`

### Unknown

Use when the answer depends on a fact the material does not provide.

Good phrasing:
- `关键事实缺失。`
- `这部分现在无法从现有资料判断。`

## Freshness Rules

1. Prefer explicit dates over implied recency.
2. Mark undated material as undated instead of guessing.
3. Judge freshness against the claim, not against the file as a whole.
4. Call out the oldest cited source when it materially affects confidence.
5. Treat a source as likely stale when:
   - a newer source addresses the same point differently
   - the source refers to an old version, policy, or state
   - the user is asking a time-sensitive question and the source date is too old for that context
6. Do not say `latest` or `current` unless the source itself or the retrieval context supports that wording.

Useful wording:
- `这份是当前引用里最旧的一份。`
- `这份资料未标日期，所以新鲜度无法确认。`
- `这里的新旧差异会直接影响结论。`
- `这份可能已经过时，但还不等于被完全推翻。`

## Conflict Types

### Factual Conflict

Two sources state different facts about the same thing.

### Time Conflict

Two sources may both be correct, but for different time windows.

### Scope Conflict

One source is talking about a narrower or broader case than the other.

### Definition Conflict

The disagreement comes from different terms, metrics, or boundaries.

### Recommendation Conflict

The facts may overlap, but the proposed action differs.

Useful wording:
- `冲突在事实层。`
- `冲突主要来自时间窗口不同。`
- `两边说的不是同一个范围。`
- `这里更像定义不一致，不是硬冲突。`

## Reliability Ordering

Do not use rigid scoring.
Instead, compare sources along these dimensions:
- directness
- date clarity
- primary vs derivative status
- specificity
- relevance to the exact claim

Preferred reasoning:
- `更新，但更像二手转述。`
- `更老，但它更直接回答这个问题。`
- `虽然时间近，但只覆盖局部情况。`

## How To Make The Final Call

1. If the evidence is strong and conflict is immaterial, give the answer directly.
2. If the evidence is mixed, narrow the claim to the part that is actually supported.
3. If conflict is unresolved and material, give a provisional answer plus the best next check.
4. If the evidence is thin, say so plainly and recommend one concrete verification step.
