# federal-immigration-expert

A generic Canadian federal immigration policy assistant (IRCC Express Entry).

Built on real-time official IRCC/canada.ca policy, supports:
- Express Entry program eligibility checks for all three programs: **CEC** (Canadian Experience Class) / **FSW** (Federal Skilled Worker, incl. the 67-point selection factors) / **FST** (Federal Skilled Trades)
- **CRS 1200 scoring** estimate (age / education / language / Canadian work experience / skill transferability / spouse / additional points: PNP 600, French, sibling, Canadian education, job offer)
- Policy update monitoring (daily cron patrol of official sources, only pushes on changes)

## Features
- Works for **any candidate**: no bound personal profile — pass background via stdin JSON
- Fully local, offline scoring — no network / no API key required
- Auto-derives NOC TEER and major occupational category from the 5-digit NOC code
- Official bilingual rule (both official languages CLB 6+ = 10 points)
- All policy judgements follow real-time official sources, never stale offline data

## Install

**Option 1 — via ClawHub CLI (recommended):**
```bash
clawhub install federal-immigration-expert --workdir ~/.openclaw/workspace
```
This downloads the skill into `~/.openclaw/workspace/skills/federal-immigration-expert/`.

**Option 2 — manual:** clone/copy this repo into the workspace skills directory so OpenClaw auto-discovers it:
```bash
git clone https://github.com/Forrest-tech/federal-immigration-expert.git \
  ~/.openclaw/workspace/skills/federal-immigration-expert
```

After installing, open a **new** OpenClaw session for the skill to be loaded.

Expected structure:
```text
federal-immigration-expert/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/       evaluator.py, policy_monitor.py, auto_discover.py
└── data/          sources.json + official IRCC snapshots
```

## Usage
```bash
echo '{"age":30,"noc":"21232","lowestCLB":9,"highestEducation":"Master","foreignYears":8,"canadaYears":1.2,"hasJobOfferLMIA":true}' | python3 scripts/evaluator.py
```
With no input it prints a demo candidate.

## Data sources (official)
- IRCC Express Entry draw history: canada.ca/.../rounds-invitations.html
- Category-based Selection: canada.ca/.../category-based-selection.html
- CEC / FSW / FST eligibility pages: canada.ca/.../who-can-apply/...
- Official snapshots: data/snapshots/ircc-cec|fsw|fst-OFFICIAL.txt (fetched 2026-08-21)

## Scripts
- `evaluator.py`: CRS + three-program eligibility + FSW 67-point table scoring engine
- `policy_monitor.py`: policy diff monitor (sanitized sha256 comparison)
- `auto_discover.py`: official source auto-discovery

## Disclaimer
Policy information is for reference only and **does not constitute immigration legal advice**. Always defer to the official IRCC decision. Policy changes over time — rely on the live official sources as the primary reference.

## License
MIT
