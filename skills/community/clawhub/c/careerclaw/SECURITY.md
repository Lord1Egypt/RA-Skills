# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in CareerClaw, please report it
responsibly. **Do not open a public GitHub issue** for security matters.

**Contact:** orestes.garcia.martinez@gmail.com
**Subject line:** `[SECURITY] CareerClaw JS — <brief description>`

Include as much detail as you can:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Affected version(s)

### Response SLA

| Severity                                                  | First response | Resolution target      | Release vehicle        |
|-----------------------------------------------------------|----------------|------------------------|------------------------|
| Critical (data exposure, key leakage)                     | < 24 hours     | < 72 hours             | Immediate patch        |
| High (pipeline hijack, file write outside `.careerclaw/`) | < 48 hours     | < 1 week               | Patch release          |
| Medium / Low                                              | < 1 week       | Next scheduled release | Patch or minor release |

You will receive an acknowledgement within the first response window. If
you do not hear back within 48 hours, follow up directly.

We do not currently offer a bug bounty program, but we will credit
responsible disclosures in the CHANGELOG unless you prefer to remain
anonymous.

---

## Security Architecture

CareerClaw is designed with a local-first, minimal-footprint security
model. The threat surface is intentionally small.

### What runs locally

Everything. CareerClaw has no backend server, no cloud endpoint, and
no telemetry pipeline. All computation — fetching, ranking, drafting,
and persistence — runs on the user's machine.

### External network calls

CareerClaw makes exactly two categories of outbound network requests:

| Destination                                    | Protocol | Auth               | Purpose                    |
|------------------------------------------------|----------|--------------------|----------------------------|
| `remoteok.com/remote-jobs.rss`                 | HTTPS    | None               | Job ingestion              |
| `hacker-news.firebaseio.com/v0/item/{id}.json` | HTTPS    | None               | Job ingestion              |
| User's configured LLM provider (optional)      | HTTPS    | User's own API key | Pro draft enhancement only |
| `api.polar.sh` (optional)                      | HTTPS    | License key hash   | Pro license validation only |

No other network calls are made. No analytics endpoints. No version-check
beacons. No callback URLs.

### Credential handling

CareerClaw touches four credential types. None are ever written to disk raw.

| Credential                    | Source      | Stored on disk?              | Logged? |
|-------------------------------|-------------|------------------------------|---------|
| `CAREERCLAW_PRO_KEY`          | Env var     | SHA-256 hash only            | Never   |
| `CAREERCLAW_ANTHROPIC_KEY`    | Env var     | Never                        | Never   |
| `CAREERCLAW_OPENAI_KEY`       | Env var     | Never                        | Never   |
| `CAREERCLAW_LLM_KEY` (legacy) | Env var     | Never                        | Never   |

Additional guarantees:
- Keys are never written to `tracking.json`, `runs.jsonl`, or any structured output
- Keys are never passed as CLI arguments (always environment variables)
- Exception messages are sanitised before propagation — keys are stripped
- `src/tests/config.test.ts` contains a dedicated test asserting that no key
  value appears in any structured output field

### License cache

When `CAREERCLAW_PRO_KEY` is first validated, only a SHA-256 hash of the key
is written to `.careerclaw/.license_cache`. The raw key is never stored.
Subsequent runs compare against the cached hash to avoid repeated network
validation calls.

### Local data

All runtime state is stored under `.careerclaw/` in the user's home directory.
This folder is gitignored by default.

| File                  | Contents                                     | Sensitive?          |
|-----------------------|----------------------------------------------|---------------------|
| `profile.json`        | Skills, roles, experience, salary range      | Yes — do not commit |
| `resume.txt`          | Full resume text                             | Yes — do not commit |
| `resume.pdf`          | Full resume (PDF)                            | Yes — do not commit |
| `tracking.json`       | Job IDs and application statuses             | Moderate            |
| `runs.jsonl`          | Anonymous run metrics (job counts, duration) | No                  |
| `.license_cache`      | SHA-256 hash of Pro key only                 | No                  |

**Never commit `.careerclaw/` to version control.** The `.gitignore`
entry is present by default — verify it before pushing.

### Source code transparency

- No obfuscated code
- No Base64-encoded URLs or network targets
- No minified scripts in the repository
- No `postinstall` hooks that execute network calls
- All dependencies declared explicitly in `package.json`

Every release is scanned with VirusTotal before publishing to ClawHub.

### Permissions

CareerClaw requests only the permissions it actually uses:

| Permission   | Used for                                      |
|--------------|-----------------------------------------------|
| `read`       | `profile.json`, `tracking.json`, resume files |
| `write`      | `tracking.json`, `runs.jsonl`                 |
| `exec`       | Running the Node.js pipeline                  |
| `web_search` | Fetching RemoteOK RSS and HN Firebase API     |

No `notification`, `cron`, or elevated permissions are requested in
the free tier.

---

## Known Limitations

**HN thread ID is manually maintained.** The Hacker News "Who is Hiring?"
thread ID in `src/config.ts` must be updated monthly. An outdated ID will
result in stale or missing results — not a security issue, but worth noting
for transparency.

**Resume text is stored in plaintext.** `.careerclaw/resume.txt` is
unencrypted. Users in shared environments should ensure appropriate
filesystem permissions on the `.careerclaw/` directory.

**LLM provider data handling.** When an LLM key is set and Pro is active,
job description excerpts and resume signal keywords are sent to the configured
provider. CareerClaw never sends the full resume text to any LLM — only the
extracted keyword signals from `ResumeIntelligence`. Review your provider's
data retention policy if this is a concern:
- Anthropic: https://www.anthropic.com/legal/privacy
- OpenAI: https://openai.com/policies/privacy-policy

---

## Supported Versions

Security fixes are applied to the latest release only. We do not backport
fixes to older versions.

| Version              | Supported |
|----------------------|-----------|
| Latest (main branch) | ✅         |
| Older releases       | ❌         |
