# careerclaw-js

[![Security Scan (VirusTotal)](https://github.com/orestes-garcia-martinez/careerclaw-js/actions/workflows/security-scan.yml/badge.svg)](https://github.com/orestes-garcia-martinez/careerclaw-js/actions/workflows/security-scan.yml)

[![CI](https://github.com/orestes-garcia-martinez/careerclaw-js/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/orestes-garcia-martinez/careerclaw-js/actions/workflows/ci.yml)

**Privacy-first job search automation for OpenClaw — Node.js / TypeScript.**

CareerClaw turns your AI agent into a structured daily workflow:
fetch listings → rank matches → draft outreach → track applications.

- **Local-first:** your resume and results stay on your machine
- **No subscription:** one-time purchase for Pro
- **Bring your own LLM API key (optional):** use OpenAI or Anthropic to enhance drafts
- **Works everywhere:** Node.js is natively available in every OpenClaw deployment

> **Why a Node.js rewrite?** The OpenClaw gateway ships Node.js v22 and npm natively,
> but has no Python package manager — making the original Python package's self-healing
> installation impossible in Docker-based deployments. careerclaw-js resolves this permanently.

---

## How It Works

1. **Fetches** job listings from RemoteOK RSS and Hacker News Who's Hiring
2. **Ranks** them against your profile using keyword overlap, experience alignment, salary fit, and work-mode preference
3. **Drafts** outreach for each top match (deterministic template on Free; LLM-enhanced on Pro)
4. **Tracks** your application pipeline locally in `.careerclaw/`

One command. Everything is local.

---

## Quickstart

### 1. Install

```bash
npm install -g careerclaw-js
```

Verify:

```bash
careerclaw-js --version
```

### 2. Set up via OpenClaw (recommended)

If you are running CareerClaw through OpenClaw/ClawHub, the agent guides you through
setup automatically. Upload your resume and it will extract your profile, ask two questions
(work mode + salary floor), and run your first briefing.

### 3. Set up manually

Create the runtime directory and profile:

```bash
mkdir -p ~/.careerclaw
```

Create `~/.careerclaw/profile.json`:

```json
{
  "skills": ["typescript", "python", "react", "sql"],
  "target_roles": ["senior engineer", "staff engineer"],
  "experience_years": 7,
  "work_mode": "remote",
  "resume_summary": "Senior engineer with 7 years building distributed systems and developer tools.",
  "location": "Austin, TX",
  "salary_min": 150000
}
```

### 4. Run your first briefing

```bash
# Dry run first — no files written, safe to preview
careerclaw-js --dry-run

# With your resume for better match quality (recommended)
careerclaw-js --resume-txt ~/.careerclaw/resume.txt --dry-run

# Full run when you're happy with the results
careerclaw-js --resume-txt ~/.careerclaw/resume.txt

# JSON output for agent/script consumption
careerclaw-js --resume-txt ~/.careerclaw/resume.txt --json
```

---

## Sample Output

```
=== CareerClaw Daily Briefing ===
Fetched jobs: 289 | Sources: remoteok: 98 | hackernews: 191
Duration: 1887ms fetch + 24ms rank

Top Matches:

1) Senior Full-Stack Engineer @ Instinct Science  [hackernews]
   score: 0.2329 | fit: 8%
   matches: react, typescript, design, aws, senior
   gaps:    elixir, postgresql, emr
   location: REMOTE (US)
   url: https://news.ycombinator.com/item?id=47233919
```

---

## Free vs Pro

| Feature | Free | Pro ($39 lifetime) |
|---|---|---|
| Daily briefing | ✅ | ✅ |
| Top 3 ranked matches | ✅ | ✅ |
| Application tracking | ✅ | ✅ |
| Outreach email draft (template) | ✅ | ✅ |
| LLM-enhanced outreach email | — | ✅ |
| Resume gap analysis | — | ✅ |
| Cover letter (tailored, <300 words) | — | ✅ coming soon |

**Pro tier: $39 one-time (lifetime license).**

Purchase: https://ogm.gumroad.com/l/careerclaw-pro

---

## Pro: Activating

Purchase a license key on Gumroad. The key is emailed immediately after payment.

### Docker / self-hosted

Add to your `.env`:

```env
CAREERCLAW_PRO_KEY=YOUR-KEY-HERE
CAREERCLAW_OPENAI_KEY=sk-...
```

### OpenClaw managed users

Tell your agent:

> "Set my CAREERCLAW_PRO_KEY to YOUR-KEY-HERE"

The key is validated against Gumroad on first use and cached locally as a SHA-256 hash.
Re-validation happens every 7 days (requires internet).

---

## Pro: LLM-Enhanced Drafts

With a valid Pro license and an LLM API key, CareerClaw writes personalised outreach emails
using your actual resume signals mapped to each job's specific requirements. Falls back to
the deterministic template silently on any LLM failure.

Failover chain example (tries Anthropic first, falls back to OpenAI):

```env
CAREERCLAW_ANTHROPIC_KEY=sk-ant-...
CAREERCLAW_OPENAI_KEY=sk-...
CAREERCLAW_LLM_CHAIN=anthropic/claude-haiku-4-5-20251001,openai/gpt-4o-mini
```

Estimated cost per run: ~$0.003 at claude-haiku-4-5-20251001 pricing (3 drafts).

---

## All CLI Options

```
careerclaw-js [OPTIONS]

Options:
  -p, --profile PATH     Path to profile.json
                         (default: .careerclaw/profile.json)
      --resume-txt PATH  Plain-text resume for enhanced matching
                         (default: .careerclaw/resume.txt if present)
  -k, --top-k INT        Number of top matches to return (default: 3)
  -d, --dry-run          Run without writing tracking or run log
  -j, --json             Machine-readable JSON output (no colour, no headers)
  -h, --help             Show this help message
```

---

## Application Tracking

Tracking is written automatically on each non-dry-run. Status lifecycle:

`saved` → `applied` → `interviewing` → `offer` → `rejected`

Runtime files — all stored under `.careerclaw/`:

| File | Contents |
|---|---|
| `profile.json` | Career profile |
| `resume.txt` | Plain-text resume (optional) |
| `tracking.json` | Saved jobs keyed by stable `job_id` |
| `runs.jsonl` | Append-only run log (one line per run) |
| `.license_cache` | Pro license validation cache (SHA-256 hash only) |

> **File format compatibility:** careerclaw-js uses the same JSON formats as the Python
> `careerclaw` package. `profile.json`, `tracking.json`, and `runs.jsonl` are fully
> interchangeable between both implementations.

---

## Environment Variables

| Variable | Description |
|---|---|
| `CAREERCLAW_PRO_KEY` | Pro license key (Gumroad) |
| `CAREERCLAW_ANTHROPIC_KEY` | Anthropic API key for LLM draft enhancement |
| `CAREERCLAW_OPENAI_KEY` | OpenAI API key for LLM draft enhancement |
| `CAREERCLAW_LLM_KEY` | Legacy single-provider key fallback |
| `CAREERCLAW_LLM_CHAIN` | Ordered failover chain, e.g. `anthropic/claude-haiku-4-5-20251001,openai/gpt-4o-mini` |
| `CAREERCLAW_LLM_MODEL` | Override default LLM model |
| `CAREERCLAW_LLM_PROVIDER` | `anthropic` or `openai` (inferred from key when not set) |
| `CAREERCLAW_DIR` | Override runtime directory (default: `.careerclaw`) |
| `HN_WHO_IS_HIRING_ID` | Override HN thread ID (updated monthly) |

Copy `.env.example` to `.env` and fill in your values.

---

## Development

### Prerequisites

- Node.js ≥ 20
- npm ≥ 10

### Setup

```bash
git clone https://github.com/orestes-garcia-martinez/careerclaw-js
cd careerclaw-js
npm install
```

### Running tests

```bash
# All tests (offline, no network)
npm test

# Watch mode
npm run test:watch

# Type-check only
npm run lint
```

### Smoke tests (live network — run before release)

```bash
npm run smoke:sources    # RemoteOK + HN connectivity
npm run smoke:briefing   # Full pipeline end-to-end
npm run smoke:llm        # LLM keys + Pro license validation
```

### Project structure

```
careerclaw-js/
├── src/
│   ├── adapters/       # RemoteOK RSS + HN Firebase adapters
│   ├── core/           # Shared text processing
│   ├── matching/       # Scoring engine
│   ├── tests/          # Vitest test suite (270 tests, fully offline)
│   ├── briefing.ts     # Pipeline orchestrator
│   ├── cli.ts          # CLI entry point
│   ├── config.ts       # Environment and source configuration
│   ├── drafting.ts     # Deterministic draft templates (Free tier)
│   ├── gap.ts          # Gap analysis engine
│   ├── license.ts      # Pro license validation (Gumroad)
│   ├── llm-enhance.ts  # LLM draft enhancement (Pro)
│   ├── models.ts       # Canonical data schemas
│   ├── requirements.ts # Job requirements extraction
│   ├── resume-intel.ts # Resume intelligence
│   ├── sources.ts      # Source aggregation
│   └── tracking.ts     # Tracking repository
├── scripts/            # Smoke + debug scripts (not published)
├── SKILL.md            # OpenClaw skill definition
├── CHANGELOG.md
├── SECURITY.md
├── package.json
└── tsconfig.json
```

---

## Security & Privacy

careerclaw-js is built on a local-first architecture.

- **No backend.** No telemetry. No analytics endpoint.
- **API keys never stored.** Keys are read from the environment at runtime only.
- **License cache is hash-only.** Only SHA-256 of the license key is written to disk.
- **LLM privacy.** Only extracted keyword signals sent to the LLM — never raw resume text.
- **External calls:** `remoteok.com`, `hacker-news.firebaseio.com`, `api.gumroad.com`,
  and your configured LLM provider (using your own key).

See [SECURITY.md](SECURITY.md) for the vulnerability disclosure policy.

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

---

## License

MIT — see [LICENSE](LICENSE)

---

## Support

- **GitHub Issues:** bug reports and feature requests
- **Response SLA:** critical bugs < 48h · general questions < 72h
- **Security disclosures:** see [SECURITY.md](SECURITY.md)
- **Pro support:** orestes.garcia.martinez@gmail.com
