# AEGIS Configuration Reference

Config file location: `~/.openclaw/aegis-config.json`

## Full Configuration Schema

```json
{
  "version": "1.0.0",

  "location": {
    "country": "AE",            // ISO 3166-1 alpha-2 country code
    "country_name": "UAE",      // Human-readable name
    "city": "Dubai",            // Your city
    "coordinates": {            // Optional, for geo-precise sources
      "lat": 25.2048,
      "lon": 55.2708
    },
    "timezone": "Asia/Dubai"    // IANA timezone string
  },

  "language": "en",             // BCP 47 language code. Briefings translated by LLM.
                                // Examples: en, ar, fr, de, zh, hi, ru, uk

  "alerts": {
    "critical_instant": true,   // Push CRITICAL alerts immediately
    "high_batch_minutes": 30,   // Batch HIGH alerts, deliver every N minutes
    "medium_digest_hours": 6,   // Include MEDIUM in digest every N hours
    "quiet_hours": {            // Optional: suppress non-critical alerts during sleep
      "enabled": false,
      "start": "23:00",         // Local time
      "end": "07:00"
    }
  },

  "briefings": {
    "morning": "07:00",         // Local time for morning briefing
    "evening": "22:00",         // Local time for evening briefing
    "enabled": true
  },

  "scan_interval_minutes": 15,  // How often to scan sources (min 5, recommended 15)

  "llm": {
    "enabled": true,            // Enable LLM verification of CRITICAL alerts (default: true)
    "provider": "ollama",       // "ollama" | "openai" | "none"
    "endpoint": "http://localhost:11434",  // LLM API base URL
    "model": "qwen3:8b",       // Model name/ID
    "api_key": "",              // API key (only needed for "openai" provider)
    "timeout": 30               // Request timeout in seconds
  },

  "api_keys": {
    "newsapi": null             // Optional: newsapi.org key (100 req/day free)
  },

  "sources": {
    "disabled": [],             // Source IDs to disable (from source-registry.json)
    "custom": []                // Add custom sources here (same schema as registry)
  },

  "filters": {
    "min_tier": 0,              // Minimum source tier to include (0=all, 3=analysis only)
    "require_location_match": true  // Only alert if content mentions your location
  },

  "tone": "factual",            // factual | detailed | minimal
  "include_preparedness": true  // Include preparedness checklist in briefings
}
```

## Minimal Configuration (Quick Start)

```json
{
  "location": { "country": "AE", "city": "Dubai", "timezone": "Asia/Dubai" },
  "language": "en",
  "alerts": { "critical_instant": true },
  "scan_interval_minutes": 15
}
```

## LLM Verification Modes

LLM verification is **optional**. Without it, AEGIS uses regex + negative pattern filtering (good accuracy). With it, CRITICAL alerts get an extra semantic check (best accuracy).

### Local Ollama (free, private)
```json
{
  "llm": { "enabled": true, "provider": "ollama", "endpoint": "http://localhost:11434", "model": "qwen3:8b" }
}
```
Requires [Ollama](https://ollama.ai) installed with a model pulled. Any model works — smaller models (1-3B) are faster, larger (8B+) are more accurate.

### OpenAI-compatible API (cloud)
```json
{
  "llm": { "enabled": true, "provider": "openai", "endpoint": "https://openrouter.ai/api", "model": "meta-llama/llama-3-8b-instruct", "api_key": "sk-or-..." }
}
```
Works with any OpenAI-compatible endpoint: OpenRouter, Together AI, Fireworks, local vLLM/LiteLLM, etc. Cost: ~$0.001 per verification.

### No LLM (regex-only)
```json
{
  "llm": { "enabled": false, "provider": "none" }
}
```
Default if no `llm` section is present. Uses regex + negative patterns only. Works well — you may see occasional false CRITICAL alerts that LLM would have caught.

## Common Country Codes

| Country | Code | Timezone |
|---------|------|----------|
| UAE | AE | Asia/Dubai |
| Israel | IL | Asia/Jerusalem |
| Lebanon | LB | Asia/Beirut |
| Ukraine | UA | Europe/Kiev |
| Poland | PL | Europe/Warsaw |
| USA | US | America/New_York |
| UK | GB | Europe/London |
| Saudi Arabia | SA | Asia/Riyadh |
| Iraq | IQ | Asia/Baghdad |

## Language Codes

| Language | Code |
|----------|------|
| English | en |
| Arabic | ar |
| French | fr |
| German | de |
| Russian | ru |
| Ukrainian | uk |
| Hebrew | he |
| Hindi | hi |
| Chinese | zh |
| Spanish | es |

## Supported Timezones

Use any [IANA timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
Common examples: `Asia/Dubai`, `Asia/Jerusalem`, `Europe/Kiev`, `America/New_York`, `Europe/London`
