---
name: access-inventory
description: Stop your AI agent from claiming it lacks access. One rule + one inventory table = no more hedging.
---

# Access Inventory

## The Problem

AI agents default to hedging. When they're unsure whether they have access to a tool, API, or service, they say "I don't have access" or "I'd need an API key for that" — even when the key is sitting in a config file two directories away.

This isn't a capability problem. It's an uncertainty problem. The agent doesn't *know* what it has, so it defaults to the safe answer: "I probably don't."

## The Fix

Two things in your `AGENTS.md`:

### 1. The Override Rule

```markdown
## ⚠️ ACCESS — NEVER CLAIM YOU LACK IT

**HARD RULE: NEVER say "I need an API key", "I don't have access", or
"I can't do that" for any tool or service.**

Instead: just TRY IT. Run the command. Read the key file. Hit the API.
If it actually fails, report the error. The answer is almost always
"you already have it."

**Default assumption: you have access to everything listed below.
Act accordingly.**
```

### 2. The Inventory Table

```markdown
### Authenticated CLIs
| Tool           | Status | Notes                        |
|----------------|--------|------------------------------|
| gh (GitHub)    | ✅     | Logged in as youruser        |
| himalaya       | ✅     | you@company.com (Fastmail)   |
| stripe         | ✅     | Key in ~/.config/stripe/     |
| supabase       | ✅     | Needs `link` per project     |

### API Keys
| Service     | Location                    |
|-------------|-----------------------------|
| Anthropic   | ~/.config/anthropic/api_key |
| OpenAI      | ~/.config/openai/api_key    |
| Replicate   | ~/.config/replicate/api_key |
| Resend      | ~/.config/resend/api_key    |

### If something's NOT listed above
1. `env | grep -i <service>`
2. `ls ~/.config/<service>/`
3. `which <tool>`
4. `brew list | grep <tool>`
5. **Only then** ask the user
```

## Why This Works

The rule removes the escape hatch — the agent can no longer punt with "I don't have access" without actually trying. The inventory removes the uncertainty — the agent knows exactly what's available and where to find it.

Together, they eliminate the most common and most frustrating agent failure pattern.

## Setup Checklist

1. Copy the override rule into your `AGENTS.md`
2. Run a discovery scan of your system:
   - `ls ~/.config/` — find API keys
   - `brew list` or `which` — find installed CLIs
   - `env | grep -i key\|token\|secret` — find env vars
3. Build your inventory table from what you find
4. Add any authenticated web services (logged-in browsers, OAuth tokens)
5. Update the inventory whenever you install or authenticate something new

## Maintenance

Review monthly. New tools get installed, keys rotate, services change. An outdated inventory is almost as bad as no inventory — it gives the agent false confidence about stale credentials.

Add this to your nightly or weekly heartbeat:

```markdown
## Access Inventory Refresh (weekly)
1. Scan for new CLIs and API keys
2. Verify existing credentials still work
3. Update AGENTS.md inventory table
4. Remove any revoked or expired entries
```
