# Remediation Guide

Fix patterns for every finding type, verified against OpenClaw v2026.3.x docs.

## Security Findings

### Inline secrets in env.vars

**Problem:** API keys stored as plaintext strings in `openclaw.json` under `env.vars`.

**Fix:** Replace with 1Password SecretRefs. First, add a secrets provider:

```json
"secrets": {
  "providers": {
    "op-gamma": {
      "source": "exec",
      "command": "/usr/local/bin/op",
      "args": ["read", "op://VaultName/ItemName/credential"],
      "passEnv": ["HOME", "OP_SERVICE_ACCOUNT_TOKEN"]
    }
  }
}
```

Then reference it in env.vars:
```json
"env": {
  "vars": {
    "GAMMA_API_KEY": {"source": "exec", "provider": "op-gamma", "id": "value"}
  }
}
```

### Plaintext bot token

**Problem:** `channels.telegram.botToken` is a raw string.

**Fix:**
```json
"channels": {
  "telegram": {
    "botToken": {"source": "exec", "provider": "op-telegram", "id": "value"}
  }
}
```

### Plaintext gateway password

**Problem:** `gateway.auth.password` is a raw string.

**Fix:**
```json
"gateway": {
  "auth": {
    "mode": "password",
    "password": {"source": "exec", "provider": "op-gateway", "id": "value"}
  }
}
```

### Unprotected .env files

**Problem:** `.env` files exist but `.gitignore` doesn't cover them.

**Fix:** Add to `.gitignore`:
```
.env
.env.*
*.env
```

---

## Cron Findings

### Jobs in error state

**Problem:** `state.lastStatus == "error"` on enabled jobs.

**Fix:** Check the job's last run output. Common causes:
- Skill dependency missing (check `requires.bins`)
- API key expired or missing
- Prompt referencing files that moved

Run the job manually to debug: trigger it via the OpenClaw dashboard or `openclaw cron run <job-id>`.

### Stale jobs

**Problem:** Enabled job hasn't run in 48+ hours (or 10+ days for weekly).

**Fix:** Check if:
- `cron.enabled` is `true` in `openclaw.json`
- The gateway is running (`openclaw gateway status`)
- The schedule expression is valid
- The job isn't blocked by `maxConcurrentRuns`

### Missing timezone

**Problem:** `schedule.tz` not set. Defaults to UTC, which shifts with DST.

**Fix:** Add timezone to each job's schedule:
```json
"schedule": {
  "kind": "cron",
  "expr": "0 9 * * *",
  "tz": "Europe/Madrid"
}
```

### Schedule conflicts

**Problem:** Multiple jobs share the same cron expression.

**Fix:** Stagger by 5-10 minutes:
```
Job A: "0 9 * * *"   ->  "0 9 * * *"
Job B: "0 9 * * *"   ->  "10 9 * * *"
```

### Missing timeout

**Problem:** `payload.timeoutSeconds` not set. Runaway jobs block subsequent runs.

**Fix:** Add a timeout to the payload:
```json
"payload": {
  "kind": "agentTurn",
  "message": "...",
  "timeoutSeconds": 300
}
```

---

## Config Findings

### No heartbeat

**Problem:** `agents.defaults.heartbeat` not configured.

**Fix:**
```json
"agents": {
  "defaults": {
    "heartbeat": {
      "every": "1h",
      "model": "sonnet",
      "prompt": "HEARTBEAT: Quick check. Report CRITICAL issues only."
    }
  }
}
```

### No model fallbacks

**Problem:** `agents.defaults.model.fallbacks` empty.

**Fix:**
```json
"agents": {
  "defaults": {
    "model": {
      "primary": "anthropic/claude-opus-4-6",
      "fallbacks": ["anthropic/claude-sonnet-4-6"]
    }
  }
}
```

### Expensive subagent model

**Problem:** No `subagents.model` set; subagents use the primary (often opus).

**Fix:**
```json
"agents": {
  "defaults": {
    "subagents": {
      "model": "sonnet",
      "maxConcurrent": 2
    }
  }
}
```

### No session maintenance

**Problem:** Old sessions accumulate without cleanup.

**Fix:**
```json
"session": {
  "maintenance": {
    "mode": "enforce",
    "pruneAfter": "7d",
    "maxEntries": 50,
    "rotateBytes": "8mb",
    "maxDiskBytes": "250mb"
  }
}
```

### No compaction

**Problem:** No context window management. Long sessions degrade quality.

**Fix:**
```json
"agents": {
  "defaults": {
    "compaction": {
      "mode": "safeguard",
      "reserveTokens": 150000,
      "keepRecentTokens": 120000
    }
  }
}
```

### No context pruning

**Problem:** Large tool results stay in context forever.

**Fix:**
```json
"agents": {
  "defaults": {
    "contextPruning": {
      "mode": "cache-ttl",
      "ttl": "4h",
      "softTrim": {"maxChars": 12000},
      "hardClear": {"enabled": true}
    }
  }
}
```

---

## Skill Quality Findings

### Missing frontmatter

Every SKILL.md must start with YAML frontmatter:
```yaml
---
name: my-skill
description: One-line description (50-200 chars) shown to the agent
---
```

### Missing metadata.openclaw

Add gating metadata as a single-line JSON in frontmatter:
```yaml
metadata: {"openclaw":{"emoji":"🔧","requires":{"bins":["python3"],"env":["MY_API_KEY"]}}}
```

### Required binary not found

If `metadata.openclaw.requires.bins` lists a binary that isn't installed, the skill won't be eligible. Install the binary or remove it from requirements.

### Scripts not executable

Run:
```bash
chmod +x skills/my-skill/scripts/*.py
chmod +x skills/my-skill/scripts/*.sh
```

### Low completeness score

Add to your SKILL.md:
- Code examples (```bash or ```json blocks)
- Command documentation
- Output format description
- Error handling guidance ("if X fails, do Y")
- Scope definition ("When to use" / "When NOT to use")

### Low clarity score

- Replace "you might want to" with "Do X"
- Add numbered steps for multi-step workflows
- Use bullet lists for options
- Add section headers (## H2) for logical grouping
