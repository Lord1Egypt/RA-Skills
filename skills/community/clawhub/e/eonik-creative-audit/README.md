# Meta Ads Creative Audit & Optimization Skill

Automated Meta Ads auditing and optimization. Detect budget leaks, halt decaying creatives, identify early scaling opportunities, and dispatch alerts to your team using AI. Clean, configurable, open-source pipeline built for OpenClaw and powered by the **eonik** logic engine.

## Features

- 💸 **Stop Budget Leaks**: Instantly detect setup and campaign structures burning budget without signal.
- 📉 **Halt Creative Decay**: Flag ads that suffer from fatigue to prevent ad-spend waste.
- 🚀 **Find Early Winners**: Identify high-potential creatives ready to scale.
- 🔒 **Zero Vendor Lock-in for Comms**: Natively integrates with Slack, Telegram, and WhatsApp via OpenCLAW's standard output router.
- 🛡️ **Enterprise DLP Grade**: Strict token ephemeral scoping and no credential logging.

## Quick Start

### 1. Install

```bash
# Install via ClawHub (recommended)
clawhub install eonik-creative-audit

# Or manual install
cd ~/.openclaw/skills/
git clone https://github.com/eonik-ai/eonik-creative-audit-skill eonik-creative-audit
cd eonik-creative-audit
```

### 2. Configure

```bash
cp config.example.json config.json
# Edit config.json with your settings
```

**Required config:**
- `meta.account_id`: Your Meta Ads Account ID (starting with `act_`)

### 3. Run Pipeline

```bash
# Make sure to securely set your key
export EONIK_API_KEY="your_api_key_here"

# Execute
python3 scripts/pipeline.py --config config.json
```

## Pipeline Stages

1. **Audit** (`audit.py`): Reaches out to the eonik AI heuristic engine using modern API keys to audit Meta Ads performance.

## Architecture

### Secure-by-Design Key Handling
All API keys, specifically the `EONIK_API_KEY`, are fetched directly from the environment inside `audit.py` and subsequently securely popped (`del os.environ["EONIK_API_KEY"]`), preventing sub-processes from inheriting or logging sensitive materials.

This explicitly remediates Data Loss Prevention (DLP) concerns from security vulnerability scans.

## Integration with OpenClaw

This skill is designed to integrate as a primary agent tool:
- You must supply the user's `act_XXXX` via natural language passing or CLI flags.
- OpenClaw workers manage the instantiation of your environmental keys dynamically before running `python3 scripts/pipeline.py`.

## Security Defaults

- `meta.redact_sensitive` defaults to `true` and should remain enabled unless explicitly approved otherwise.
- Use explicit account scoping with `meta.account_id` (must start with `act_`) before running audits.
- Auto-resolving account scope is disabled by default and should only be enabled with explicit opt-in.

## Cron Integration

Cron scheduling is opt-in only. Enable scheduled audits only with explicit approval from the account owner/security approver:

```bash
openclaw cron add --name "daily-eonik-audit" --cron "0 8 * * *" --message "Run the eonik ad audit pipeline" --session isolated
```

## Dependencies

**Core (included):**
- Python 3.7+
- Standard library only

**Not required:**
- Zero external packages like `requests`, `pyyaml`, or `slack_sdk` (uses standard `urllib` and `json`).

Zero external dependencies by design, ensuring frictionless installations on enterprise worker nodes.

## File Structure

```
eonik-creative-audit/
├── SKILL.md              # Skill metadata and triggers
├── README.md             # This file
├── config.example.json   # Configuration template
├── scripts/
│   ├── pipeline.py       # Full orchestrator
│   └── audit.py          # Ad audit execution
└── output/               # Generated reports (auto-created)
```
