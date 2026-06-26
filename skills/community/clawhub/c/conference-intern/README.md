# 🎪 Conference Intern

**Your AI-powered side event concierge for crypto conferences.**

Conference Intern discovers, curates, and auto-registers you for side events at crypto conferences. It scrapes events from [Luma](https://lu.ma) pages and community-curated Google Sheets, filters them using your preferences with LLM intelligence, and handles Luma RSVP via browser automation — so you spend less time juggling event pages and more time networking.

> An [OpenClaw](https://openclaw.com) skill — requires an OpenClaw agent with browser access.

---

## How It Works

Conference Intern runs a four-stage pipeline, each stage independent and re-runnable:

```
Setup → Discover → Curate → Register
                ↑                 │
                └── Monitor ──────┘
```

1. **Setup** — interactive walkthrough to configure your conference: event source URLs, interest topics, avoid list, registration strategy
2. **Discover** — fetches events from Luma and Google Sheets, validates RSVP URLs, normalizes them into a unified `events.json`
3. **Curate** — LLM scores and ranks events based on your preferences, outputs a tiered schedule (`curated.md`)
4. **Register** — script-driven loop that calls the agent once per event, ensuring every event is attempted. Two-pass flow handles custom fields.
5. **Monitor** — re-runs discover + curate on a schedule, flags newly added events

## Getting Started

Once the skill is installed in your OpenClaw agent, just talk to it. Here are some example prompts:

> **"Set me up for EthCC 2026"**
> Kicks off the interactive setup — the agent will ask you for Luma URLs, Google Sheet links, your interests, and registration preferences.

> **"Find side events for ethcc-2026"**
> Discovers events from all your configured sources.

> **"Curate my ethcc-2026 events"**
> Scores and ranks discovered events based on your preferences, outputs a tiered schedule.

> **"Register me for the recommended ethcc-2026 events"**
> Auto-RSVPs on Luma for your curated picks via browser automation.

> **"Check for new ethcc-2026 events"**
> Re-runs discovery and curation, flags anything new since last time.

## What You Get

After running the pipeline, you get a `curated.md` schedule like this:

```markdown
# EthCC 2026 — Side Events

Last updated: 2026-07-08 14:00 UTC
Strategy: aggressive | Events: 47 found, 31 recommended

## July 8 (Wednesday)

### Must Attend
- **ZK Privacy Summit** — 14:00-18:00 @ Maison de la Mutualité
  Host: PrivacyDAO | RSVPs: 234
  ✅ Registered

### Recommended
- **DeFi Builders Happy Hour** — 18:00-21:00 @ Le Comptoir
  Host: DeFi Alliance | RSVPs: 89
  ⏳ Needs input: [Company name, Role]

### Optional
- **Infra Roundtable** — 10:00-12:00 @ Hotel Conf Room
  Host: InfraDAO
  🔗 Register manually

## Blocked / Filtered Out
- ~~NFT Minting Party~~ — matched avoid list: "NFT minting parties"
```

## Configuration

Setup creates a `config.json` per conference where you define:

- **Source URLs** — Luma event pages and Google Sheets links
- **Interests** — topics you care about (e.g., "DeFi", "ZK proofs", "MEV")
- **Avoid list** — topics to filter out (e.g., "token launches")
- **Blocked organizers** — specific hosts to exclude
- **Strategy** — `aggressive` (register broadly) or `conservative` (only top-tier events)
- **Monitoring** — `scheduled` (automatic), `on-demand`, or `both`
- **Luma auth** — optional login via email 2FA for faster RSVPs

## Project Structure

```
conference-intern/
├── SKILL.md                        # Skill metadata + agent instructions
├── luma-knowledge.md               # Shared Luma page patterns (learned by agent)
├── scripts/
│   ├── common.sh                   # Shared helpers (URL validation, MD parsing, etc.)
│   ├── setup.sh                    # Interactive setup
│   ├── discover.sh                 # Event discovery + link validation
│   ├── curate.sh                   # LLM-powered curation
│   ├── register.sh                 # Script-driven RSVP loop
│   └── monitor.sh                  # New event detection
├── templates/
│   ├── setup-prompt.md             # Agent prompt for setup flow
│   ├── curate-prompt.md            # Agent prompt for event scoring
│   ├── register-prompt.md          # Agent prompt for RSVP (legacy, reference only)
│   └── register-single-prompt.md   # Agent prompt for single-event RSVP
└── conferences/
    └── {conference-id}/            # Per-conference runtime data (gitignored)
        ├── config.json
        ├── events.json
        ├── curated.md
        ├── luma-session.json
        └── custom-answers.json     # User answers to custom RSVP fields
```

## Event Sources

### Luma
The script opens Luma calendar pages directly via the OpenClaw browser CLI, scrolls to load all events (infinite scroll), then extracts everything in one bulk JavaScript call. No agent context window needed — fast, reliable, handles 150+ events in seconds.

### Google Sheets
Community-curated spreadsheets (commonly shared on Telegram/Twitter before conferences) are read via browser automation — the agent opens the sheet and extracts event rows directly.

## Smart Registration

Registration is driven by a bash script that loops over events, using CLI browser commands for each one. The agent is only called for fuzzy-matching custom field labels (~5-10s text-only) — all browser work is handled by the CLI.

- **Hybrid CLI + agent** — CLI opens pages, clicks buttons, fills forms, submits. Agent only matches custom field labels to your answers.
- **Two-pass flow** — pass 1 registers what it can, pass 2 retries events that need custom field answers
- **Fills only mandatory fields** — never guesses optional or custom fields
- **Deduplicated custom fields** — if 3 events ask for "Company", you answer once. Answers are saved in `custom-answers.json` and reused across re-runs
- **Link validation** — RSVP URLs are validated during discovery; dead links (404s) are filtered out before registration
- **CAPTCHA and session expiry stop the loop** — instead of continuing into repeated failures
- **Already-registered detection** — if you registered manually, the agent notices and moves on
- **Session cookies are persisted** so you don't re-authenticate every run

### CLI Flags

```bash
# Register for all pending events
bash scripts/register.sh my-conference

# Retry only events that need custom field answers
bash scripts/register.sh my-conference --retry-pending

# Override delay between events (default: 5 seconds)
bash scripts/register.sh my-conference --delay 10
```

## Requirements

- [OpenClaw](https://openclaw.com) with browser capability
- [`jq`](https://jqlang.github.io/jq/) for JSON processing
- `python3` for event scoring and markdown generation
- `curl` for URL validation
- `sha256sum` for event ID generation (standard on Linux, use `shasum` on macOS)

## Data & Privacy

This skill stores per-conference data in your OpenClaw workspace (`~/.openclaw/workspace/conferences/<id>/`):

- **config.json** — your conference preferences (interests, strategy, source URLs)
- **events.json** — discovered event data (names, dates, URLs, hosts)
- **curated.md** — scored and tiered event schedule
- **luma-session.json** — Luma browser session cookies (optional — see below)
- **custom-answers.json** — your answers to custom registration fields (company, role, etc.)
- **registration-status.json** — batch progress tracker

The skill also reads `~/.openclaw/openclaw.json` to detect your workspace path.

**Luma authentication is optional.** You can log into Luma in the OpenClaw browser for faster registration (name and email are pre-filled). But if you prefer not to persist a Luma session, the skill works without it — the agent will type your name and email from `config.json` each time. Session cookies (`luma-session.json`) are only created if you choose to log in and can be deleted at any time.

**What touches the network:**
- **Luma and Google Sheets** are accessed through the browser (same as manual browsing)
- **Your OpenClaw agent's LLM** receives event data and preferences for curation and form-filling — this goes to whatever model provider you've configured (e.g., OpenAI). No additional external services are contacted beyond your agent's LLM and the event source websites.
- **All file operations are local** — results are written to your workspace, not uploaded anywhere.

## Design Principles

- **Evergreen** — browser extraction adapts to page changes; no hardcoded API calls
- **Agent-agnostic** — works with any OpenClaw agent that has browser access
- **Re-runnable** — every pipeline stage is idempotent; safe to re-run after partial failures
- **User in control** — never guesses answers for custom fields; always defers to you
- **Bash controls the loop** — the agent handles one event at a time; the script ensures all events are attempted

## Contributing

Pull requests are welcome! If you have ideas for new event sources, better curation heuristics, or support for additional conference platforms, feel free to open a PR.

## License

MIT
