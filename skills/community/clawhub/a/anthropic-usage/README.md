# Anthropic Usage Skill

[![version](https://img.shields.io/badge/version-1.0.7-blue)](https://clawhub.ai/leaofelipe/anthropic-usage)

An [OpenClaw](https://openclaw.dev) Agent Skill that queries the **Anthropic Admin API** to display token usage reports — daily, weekly, monthly, and broken down by model.

---

## What it does

- Fetches token consumption data from the Anthropic Admin API
- Reports uncached input tokens, cache read/creation tokens, output tokens, and totals
- Supports daily, weekly, and monthly windows
- Optionally groups results by model (e.g. Opus vs Sonnet vs Haiku)
- Automatically follows API pagination — all pages are merged before rendering
- Outputs clean, markdown-friendly tables you can read in the terminal or in chat

---

## Prerequisites

> **IMPORTANT: Organization account required**
>
> The Anthropic usage report API (`/v1/organizations/usage_report/messages`) is only
> available to accounts on an **Anthropic Organization plan**. If your account is on the
> free tier or a personal plan, the API will return a `403 Forbidden` error.
>
> You also need an **Admin API key**, not a regular API key. Admin keys are generated in
> the Anthropic Console under **Settings → API Keys → Admin keys**.

You need the following tools installed locally:

| Tool   | Why                                  | Check            |
| ------ | ------------------------------------ | ---------------- |
| `curl` | Makes HTTP requests to the API       | `curl --version` |
| `jq`   | Parses and transforms JSON responses | `jq --version`   |

Install `jq` if missing:

- **Ubuntu/Debian**: `sudo apt install jq`
- **macOS**: `brew install jq`
- **Fedora/RHEL**: `sudo dnf install jq`

---

## Installation

### Via clawhub (recommended)

```bash
clawhub install anthropic-usage
```

### Manual

```bash
git clone https://github.com/leaofelipe/anthropic-usage.git
cd anthropic-usage
chmod +x scripts/usage.sh
```

---

## Setting up your API key

This skill requires an Anthropic **Admin API key**. Your account must be on an **Organization plan** — personal accounts get a `403 Forbidden`.

You can generate an Admin API key in the Anthropic Console under **Settings → API Keys → Admin keys**.

### Option 1 — OpenClaw UI (recommended)

1. Open the OpenClaw UI and go to the **Skills** section
2. Find **anthropic-usage** and click on it
3. Enter your Admin API key in the **API key** field and click **Save key**

That's it — no config file editing needed.

### Option 2 — Edit `openclaw.json` directly (for CLI users)

Open `~/.openclaw/openclaw.json` and add your key under the skill entry:

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

> **Your key is stored in `~/.openclaw/openclaw.json` and never leaves your machine.**

Once the key is saved, verify it works:

```bash
bash scripts/usage.sh --check
```

---

## Usage

### In chat (via OpenClaw)

Simply ask naturally:

```
Show me my Anthropic token usage for today
How much have I used this week?
Give me a monthly breakdown by model
What models am I using the most this month?
How much did I spend this week?
```

> **Cost estimation:** When you ask about costs, the agent automatically fetches the current Anthropic pricing page to ensure the rates used in the calculation are always up to date.

### Directly in the terminal

Make sure the script is executable:

```bash
chmod +x scripts/usage.sh
```

Available flags:

| Flag          | Description                                         |
| ------------- | --------------------------------------------------- |
| `--daily`     | Show today's usage                                  |
| `--weekly`    | Show the past 7 days (default if no flag given)     |
| `--monthly`   | Show the past 30 days                               |
| `--breakdown` | Group results by model                              |
| `--check`     | Verify the API key is valid (no usage data fetched) |
| `--help`      | Show help text                                      |

Flags can be combined:

```bash
# Today's usage
bash scripts/usage.sh --daily

# Past 7 days
bash scripts/usage.sh --weekly

# Past 30 days
bash scripts/usage.sh --monthly

# Past 7 days, broken down by model
bash scripts/usage.sh --weekly --breakdown

# Past 30 days, broken down by model
bash scripts/usage.sh --monthly --breakdown

# Multiple periods at once — each section is printed in sequence
bash scripts/usage.sh --daily --weekly --monthly
```

> **Tip:** Period flags (`--daily`, `--weekly`, `--monthly`) can be combined freely.
> Each requested period is fetched and rendered as a separate section in the output.
> `--breakdown` applies to all requested periods simultaneously.

### Example output

```
Querying Anthropic usage API...

## Usage — past 7 days

| Metric                  | Value                        |
|-------------------------|------------------------------|
| Uncached input tokens   | 10,200,000                   |
| Cache read tokens       |  1,900,000                   |
| Cache creation tokens   |    350,000                   |
| Total input tokens      | 12,450,000                   |
| Output tokens           |  1,830,000                   |
| Total tokens            | 14,280,000                   |
| Web search requests     |            42                |

Done.
```

With `--breakdown`:

```
## Usage — past 7 days — by model

| Model                                    | Input tokens  | Output tokens | Web searches |
|------------------------------------------|---------------|---------------|--------------|
| claude-opus-4-6                          |     8,200,000 |     1,100,000 |           30 |
| claude-sonnet-4-6                        |     3,900,000 |       680,000 |           12 |
| claude-haiku-4-5-20251001                |       350,000 |        50,000 |            0 |
```

---

## Verification

After setting up your API key, verify it works before running any usage queries:

```bash
bash scripts/usage.sh --check
```

Expected output on success:

```
Checking API key...
OK — key is valid (verified via /v1/models). Note: usage endpoint permissions are only confirmed when fetching data.
```

What each outcome means:

| Output                 | Meaning                                                                | Action                                                                                  |
| ---------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `OK — key is valid...` | Key is accepted by the API                                             | You are good to go                                                                      |
| `401 Unauthorized`     | Key is invalid, expired, or has a typo                                 | Re-generate the key in the Anthropic Console and update `~/.openclaw/openclaw.json`     |
| `403 Forbidden`        | Key lacks required permissions, or account is not on Organization plan | Ensure you are using an **Admin key** and that your account is on the Organization plan |
| `Network error`        | `curl` could not reach `api.anthropic.com`                             | Check your internet connection                                                          |

---

## Pagination

The script automatically follows API pagination. If the API returns multiple pages of
results, they are fetched sequentially and merged into a single dataset before rendering.

The following safeguards prevent the script from hanging or looping indefinitely:

| Scenario                                           | Protection                                                  | Max wait                 |
| -------------------------------------------------- | ----------------------------------------------------------- | ------------------------ |
| DNS does not resolve / API unreachable             | `--connect-timeout 10` on every `curl` call                 | 10 s                     |
| Connection open but API stops sending data         | `--max-time 30` on every `curl` call                        | 30 s                     |
| API returns `has_more: true` indefinitely          | Hard limit of 100 pages per request                         | 100 × 30 s (theoretical) |
| API returns `has_more: true` but empty `next_page` | Explicit `-z "$next_page"` check exits the loop immediately | Immediate                |

In practice, a 30-day window with `bucket_width=1d` fits in a single page (the API
returns at most 31 buckets per page). Reaching the 100-page limit would require a
severely malformed API response.

---

## Troubleshooting

**"ANTHROPIC_ADMIN_API_KEY is not set"**
The key is missing. Set it via the OpenClaw UI (**Skills → anthropic-usage → API key**) or by editing `~/.openclaw/openclaw.json` directly. See the [Setting up your API key](#setting-up-your-api-key) section above.

**"401 Unauthorized"**
Your key is invalid or expired. Generate a new one from the Anthropic Console and update it in `~/.openclaw/openclaw.json`.

**"403 Forbidden"**
One of two things:

1. You are using a regular API key instead of an **Admin key**.
2. Your Anthropic account is not on an Organization plan.

**"jq: command not found"**
Install `jq` — see the [Prerequisites](#prerequisites) section.

**"Network error: curl failed (timed out or connection refused)"**
The API did not respond within 30 seconds. Check your internet connection and try again.
If the problem persists, verify the Anthropic API status at [status.anthropic.com](https://status.anthropic.com).

**"Pagination safety limit reached"**
The script fetched 100 pages without reaching the end of the results. This should never
happen under normal conditions — it likely indicates a bug in the API response. Open an
issue with the raw API response if you encounter this.

---

## Testing

Run the test suite with no credentials or network access required:

```bash
bash tests/run_tests.sh
```

Tests use a curl stub that intercepts all HTTP calls and returns fixture responses from `tests/fixtures/`. The suite covers argument parsing, token aggregation, HTTP error handling, pagination, and key security.

---

## Contributing

Pull requests are welcome. Please:

1. Keep the script POSIX-compatible where possible
2. Test on both Linux (GNU date) and macOS (BSD date)
3. Do not add Python or Node dependencies — `curl` + `jq` only
4. Never store or log API keys

---

## License

MIT-0 (MIT No Attribution). See [LICENSE](LICENSE).
