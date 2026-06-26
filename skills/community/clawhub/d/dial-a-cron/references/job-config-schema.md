# Job Config Schema Reference

## Full Schema

```json
{
  "jobId": "string (required, matches filename)",
  "description": "string (human-readable)",
  "skipIfNoDiff": "boolean (default: false)",
  
  "diffs": [
    {
      "type": "file | http | command",
      "path": "string (for file type)",
      "url": "string (for http type)",
      "cmd": "string (for command type)",
      "jq": "string (dot-notation for JSON extraction, http only)",
      "label": "string (human-readable name)"
    }
  ],
  
  "routes": [
    {
      "to": "string (target name: bobby, faceman, log, silent)",
      "channel": "string (telegram | a2a | webhook | file | email | log | silent)",
      "when": ["string (severity: silent | log | info | alert | urgent | >=info)"],
      "match": ["string (keyword/regex to match on output)"],
      "target_id": "string (chat ID, URL, file path, email address, agent ID)"
    }
  ],
  
  "budget": {
    "maxTokensPerRun": "number (default: 50000)",
    "maxTokensPerMonth": "number (default: 500000)",
    "onBudgetExceeded": "string (downgrade | skip | alert)",
    "downgradeModel": "string (model to use when over budget)",
    "alertAt": "number (percent, default: 80)"
  },
  
  "chain": {
    "onComplete": [
      {
        "trigger": "string (condition: severity >= info)",
        "target": "string (job-id to trigger)",
        "message": "string (template with {{output.summary}})"
      }
    ],
    "onError": [
      {
        "trigger": "string (condition: consecutiveErrors >= 2)",
        "target": "string (job-id or agent)",
        "message": "string"
      }
    ]
  }
}
```

## Channel Reference

| Channel | target_id | Example |
|---|---|---|
| `telegram` | Telegram chat ID or username | `"8301484123"` or `"-1003820115039"` |
| `a2a` | Agent name or endpoint | `"faceman"` or `"http://192.168.1.225:18800/a2a"` |
| `webhook` | HTTP(S) URL | `"https://hooks.slack.com/services/T.../B.../xxx"` |
| `file` | Local file path | `"reports/daily.md"` or `"/var/log/cron-reports.md"` |
| `email` | Email address (requires gog) | `"team@example.com"` |
| `log` | Auto: `logs/{job-id}.log` | N/A |
| `silent` | State file only | N/A |

## Severity Matching

Routes use `when` arrays. Special prefix `>=` matches that severity and above:

- `["alert", "urgent"]` — only alert and urgent
- `[">=info"]` — info, alert, and urgent
- `[">=silent"]` — everything (all levels)

## Content Matching

Routes use `match` arrays with keyword/regex patterns:

- `["revenue", "demo"]` — matches if output contains "revenue" OR "demo"
- `["corpus|ingest"]` — regex OR pattern
- `[]` or omitted — matches all content
