---
name: anthropic-usage
description: "Query Anthropic Admin API for token usage reports (daily, weekly, monthly) with model breakdown. Requires an Anthropic Organization account. Configure your Admin API key via the skill's API key field in the OpenClaw UI."
metadata:
  openclaw:
    emoji: 📊
    primaryEnv: ANTHROPIC_ADMIN_API_KEY
    requires:
      bins:
        - curl
        - jq
      env:
        - ANTHROPIC_ADMIN_API_KEY
---

# anthropic-usage

You are helping the user query their Anthropic token usage via the Admin API.

## Before running anything

Check whether the API key is available:

```bash
[[ -n "${ANTHROPIC_ADMIN_API_KEY:-}" ]] && echo "KEY_EXISTS" || echo "KEY_MISSING"
```

- If the output is `KEY_MISSING`: stop and guide the user through setup. Do NOT proceed until the variable is set.
- If the output is `KEY_EXISTS`: proceed.

### Setup guidance (show this when KEY_MISSING)

Tell the user they have two options:

**Option 1 (recommended) — OpenClaw UI:**
Open the OpenClaw UI, go to **Skills → anthropic-usage**, enter the Admin API key in the **API key** field, and click **Save key**.

**Option 2 — Edit `~/.openclaw/openclaw.json` directly (for CLI users):**
Add the key under the skill entry:

```json
{
  "skills": {
    "entries": {
      "anthropic-usage": {
        "enabled": true,
        "apiKey": "sk-ant-admin-..."
      }
    }
  }
}
```

The gateway picks up the change automatically — no restart needed.

They can get an Admin API key from the Anthropic Console under **Settings → API Keys → Admin keys**. Their account must be on an **Organization plan** to access usage reports.

## Running the usage script

Once the key exists, run `scripts/usage.sh` with the appropriate flags based on what the user asked for:

| User intent | Command |
|---|---|
| Today's usage | `bash scripts/usage.sh --daily` |
| This week | `bash scripts/usage.sh --weekly` |
| This month | `bash scripts/usage.sh --monthly` |
| Breakdown by model | `bash scripts/usage.sh --breakdown` |
| Weekly + model breakdown | `bash scripts/usage.sh --weekly --breakdown` |
| Monthly + model breakdown | `bash scripts/usage.sh --monthly --breakdown` |

Run the command from the skill's root directory (where `scripts/` lives), or use the full path to `scripts/usage.sh`.

## Formatting the output

After the script runs:

1. Present the data as a **friendly chat message**, not a raw dump.
2. Summarize the key numbers at the top (total input tokens, total output tokens).
3. If `--breakdown` was used, render the per-model table in a readable way.
4. **Estimate the cost (agent-side step):** The script returns token counts only — pricing is not included. After presenting the token data, use your `web_fetch` tool to fetch `https://www.anthropic.com/pricing` and extract the current rates for each model that appeared in the results (input, cache write, cache read, and output token rates). Calculate the estimated cost per model and the total. Present this as a cost summary after the token table. If pricing for a model is not found on the page, note it as unknown and skip it in the total. This fetch is intentional and scoped to `anthropic.com`.
5. If the script exits with an error (non-zero exit code), show the error message and suggest fixes:
   - Exit 1 / "key file not found" → re-show setup guidance
   - "401 Unauthorized" → key is invalid or expired
   - "403 Forbidden" → key lacks Admin permissions or account is not on an Organization plan
   - Network error → ask the user to check their internet connection

## Example friendly output

```
Here's your Anthropic usage for the past 7 days:

📥 Input tokens:   12,450,000
📤 Output tokens:    1,830,000
🔢 Total tokens:   14,280,000

Model breakdown:
| Model                     | Input tokens | Output tokens |
|---------------------------|-------------|---------------|
| claude-opus-4-6           |   8,200,000 |   1,100,000   |
| claude-sonnet-4-6         |   3,900,000 |     680,000   |
| claude-haiku-4-5-20251001 |     350,000 |      50,000   |

💰 Estimated cost (prices fetched live from anthropic.com/pricing):
| Model                     | Estimated cost |
|---------------------------|----------------|
| claude-opus-4-6           |        $152.40 |
| claude-sonnet-4-6         |         $18.72 |
| claude-haiku-4-5-20251001 |          $0.53 |
| **Total**                 |    **$171.65** |
```

Keep the tone helpful and concise.
