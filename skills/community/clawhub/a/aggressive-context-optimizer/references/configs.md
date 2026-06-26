# Config examples

## Fix 1: Shrink bootstrap files

```json
{
  "agents": {
    "defaults": {
      "bootstrapMaxChars": 3000,
      "bootstrapTotalMaxChars": 12000,
      "imageMaxDimensionPx": 768
    }
  }
}
```

## Fix 2: Throttle tool output

```json
{
  "tools": {
    "web": {
      "search": { "maxResults": 3 },
      "fetch": { "maxCharsCap": 4000 }
    }
  }
}
```

## Fix 3: Prune stale tool results

```json
{
  "agents": {
    "defaults": {
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "30m",
        "keepLastAssistants": 3,
        "minPrunableToolChars": 500
      }
    }
  }
}
```

## Fix 4: Tighten memory retrieval

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "query": {
          "maxResults": 3,
          "minScore": 0.75,
          "hybrid": {
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": true, "halfLifeDays": 14 }
          }
        }
      }
    }
  }
}
```

## Fix 5: Automatic compaction

```json
{
  "agents": {
    "defaults": {
      "compaction": { "enabled": true }
    }
  }
}
```
