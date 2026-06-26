# Model Selection — When to Use Each Variant

## Decision Matrix

| Use Case | Recommended Model | Reason |
|----------|------------------|--------|
| Research & data collection | Default (qwen/gpt equivalent) | Cost-effective, sufficient for factual work |
| Creative writing | Model with better creative capabilities | Quality matters for user-facing content |
| Code generation | Codex/Codex-like model | Specialized for code, faster iteration |
| Complex analysis | Strong reasoning model | Better for multi-step logic |
| Quick summaries | Lightweight model | Fast, cheap, good enough |
| Long documents | Model with large context window | Can handle full text in one pass |

## Cost vs. Quality Tradeoff

```
Simple subtask (search, list, summarize) → cheapest model
Medium subtask (analyze, compare, draft) → standard model
Complex subtask (code, creative, multi-step) → strongest model
```

## Heuristic Rules

1. **Research subtasks** always use cheapest model (facts are facts)
2. **Writing subtasks** use standard model (quality matters for tone)
3. **Code subtasks** use capable coding model (errors cost more than model cost)
4. **Synthesis step** always uses strongest model (this is the value-add)
5. **Review/verify subtasks** use standard model (need accuracy, not creativity)
