# Cognition — Tier 2 Retrieval Configuration

These settings are **Tier 2 (advanced)** recommendations for users running hybrid retrieval.
They are not required for Tier 0 manual retrieval or Tier 1 keyword search.

Add these settings to your `openclaw.json` under `agents.defaults` if you want higher-quality retrieval.

## Compaction & Memory Flush

```json
"compaction": {
  "reserveTokensFloor": 40000,
  "memoryFlush": {
    "enabled": true,
    "softThresholdTokens": 4000,
    "systemPrompt": "Session nearing compaction. Store durable memories now.",
    "prompt": "Write any lasting notes to memory/YYYY-MM-DD.md; reply with NO_REPLY if nothing to store."
  }
}
```

## Hybrid Search

```json
"memorySearch": {
  "enabled": true,
  "query": {
    "maxResults": 8,
    "hybrid": {
      "enabled": true,
      "vectorWeight": 0.7,
      "textWeight": 0.3,
      "candidateMultiplier": 4,
      "mmr": {
        "enabled": true,
        "lambda": 0.7
      },
      "temporalDecay": {
        "enabled": true,
        "halfLifeDays": 30
      }
    }
  },
  "cache": {
    "enabled": true,
    "maxEntries": 50000
  }
}
```

## Context Pruning

```json
"contextPruning": {
  "mode": "cache-ttl",
  "ttl": "5m"
}
```

## Notes

- `vectorWeight 0.7 / textWeight 0.3` is a practical default, not gospel.
- MMR helps diversify near-duplicate search hits.
- Temporal decay is a Tier 2 optimization; evergreen files may need custom handling.
- If you are not running embeddings, skip this file and use the Retrieval Tiers in `SKILL.md`.
