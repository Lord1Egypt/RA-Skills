# Agent Configuration

Each agent can have a `config.json` for persistent settings that survive across sessions.

## Structure

```
agents/[name]/config.json
```

## Purpose

- **First-run detection**: If `setup_complete` is false, prompt the user for initial preferences
- **Persistent preferences**: Store settings that don't belong in SOUL.md (too granular or frequently changing)
- **API key references**: Point to Keychain entries, never store actual keys
- **Custom thresholds**: Agent-specific numbers (word count targets, price ranges, etc.)

## First-Run Flow

1. Agent checks `config.json` on activation
2. If `setup_complete` is false, ask user for essential preferences
3. Save preferences and set `setup_complete` to true
4. On subsequent runs, read preferences silently

## Examples by Role

### Research Agent
```json
{
  "agent_name": "Scout",
  "setup_complete": true,
  "preferences": {
    "preferred_sources": ["reuters", "bloomberg", "techcrunch"],
    "language_priority": ["en", "ar"],
    "max_source_age_days": 7
  },
  "api_keys_ref": ["keychain:openclaw-x-api"],
  "custom_settings": {
    "min_sources_per_report": 3
  }
}
```

### Content Agent
```json
{
  "agent_name": "Pen",
  "setup_complete": true,
  "preferences": {
    "default_tone": "casual-professional",
    "target_platform": "twitter",
    "prohibited_words": ["delve", "landscape", "leverage"]
  },
  "api_keys_ref": [],
  "custom_settings": {
    "tweet_max_chars": 280,
    "thread_max_tweets": 15
  }
}
```

### Dev Agent
```json
{
  "agent_name": "Forge",
  "setup_complete": true,
  "preferences": {
    "language": "swift",
    "style_guide": "apple-swift-style",
    "test_framework": "XCTest"
  },
  "api_keys_ref": ["keychain:github-token"],
  "custom_settings": {
    "max_pr_size_lines": 500
  }
}
```

## Rules

1. Never store actual API keys or secrets in config.json
2. Use `api_keys_ref` to point to Keychain service names
3. Keep preferences minimal: only what changes agent behavior
4. Config changes should be logged in the agent's memory
