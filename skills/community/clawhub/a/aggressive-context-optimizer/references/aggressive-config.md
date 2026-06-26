# Aggressive all-in-one config

Use this when the user wants maximum token savings and is willing to loosen settings later if quality drops.

```json
{
  "agents": {
    "defaults": {
      "bootstrapMaxChars": 2500,
      "bootstrapTotalMaxChars": 10000,
      "imageMaxDimensionPx": 512,
      "compaction": { "enabled": true },
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "15m",
        "keepLastAssistants": 2,
        "minPrunableToolChars": 300
      },
      "memorySearch": {
        "query": {
          "maxResults": 2,
          "minScore": 0.8,
          "hybrid": {
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": true, "halfLifeDays": 7 }
          }
        }
      }
    }
  },
  "tools": {
    "web": {
      "search": { "maxResults": 2 },
      "fetch": { "maxCharsCap": 3000 }
    }
  }
}
```
