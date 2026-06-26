# Garmin Frisbee Analysis - Clawdbot Skill

> **Ultimate Frisbee performance analytics powered by Garmin data** — "how many sprints did I hit in yesterday's game?", "was my recovery fast enough between points?", "am I more fatigued than last tournament?"

Analyze sprint count & fatigue, top speed, heart rate zones, Body Battery, HRV trends, sleep quality, and generate interactive dashboards. Compare tournaments vs. training, and track season-long fitness trends. Built for competitive Ultimate Frisbee players.

## 🔵 Looking for Claude Desktop?

**This is the Clawdbot skill repo.** For standard Claude Desktop, use the dedicated MCP server:

👉 **[MCP Setup Guide](references/mcp_setup.md)** - Claude Desktop setup instructions

---

## 🚀 Clawdbot Installation

**Best for**: Post-game analysis, tournament fatigue tracking, proactive health check-ins

```bash
# Install via clawdhub
clawdhub install garmin-frisbee-analysis

# Or manually
cd ~/.clawdbot/skills
git clone https://github.com/EvelynDevelops/garmin-frisbee-analysis.git garmin-frisbee-analysis

# Install dependencies (versions pinned in requirements.txt)
pip3 install -r requirements.txt

# Configure credentials and authenticate
python3 scripts/garmin_auth.py login
```

**[📖 Full Setup Guide](SKILL.md)**

## ⚡ Features

- **Sprint analysis**: Count, top speed, fatigue index (last 3 vs first 3 sprint peaks)
- **Post-game dashboards**: Speed timeline, sprint bands, HR zone distribution
- **Tournament review**: Body Battery fatigue curve, HRR curves, overnight sleep/HRV
- **Season comparisons**: Training vs game intensity, top speed trends, volume over time
- **General health**: Sleep stages, Body Battery, HRV, resting HR, stress levels
- **Activity files**: Download FIT/GPX for detailed route and performance analysis

## 📊 Example Queries

> "How many sprints did I hit in yesterday's game?"
>
> "Was my sprint speed dropping by the end?"
>
> "Show me my tournament fatigue curve"
>
> "How did I sleep during the tournament?"
>
> "Am I improving this season?"

## 📦 What's Included

```
garmin-frisbee-analysis/
├── SKILL.md                          # Clawdbot setup & usage
├── README.md                         # This file
├── requirements.txt                  # Pinned Python dependencies
├── install.sh                        # Automated installation script
├── scripts/
│   ├── garmin_auth.py               # Authentication helper
│   ├── garmin_data.py               # Fetch health metrics (JSON)
│   ├── garmin_chart.py              # Generate HTML charts
│   ├── frisbee_activity.py          # Post-game analysis dashboard
│   ├── frisbee_tournament.py        # Tournament review dashboard
│   └── frisbee_compare.py           # Comparison & season analysis
└── references/
    ├── health_analysis.md           # Metric interpretation guide
    ├── api.md                       # Garmin Connect API docs
    ├── mcp_setup.md                 # Claude Desktop MCP setup
    └── extended_capabilities.md     # Advanced features
```

## 🔒 Privacy & Security

This skill requires `GARMIN_EMAIL` and `GARMIN_PASSWORD` to authenticate with Garmin Connect.

- **Password**: never written to disk or logged — used only during the authentication step, then discarded
- **Session tokens**: stored locally in `~/.clawdbot/garmin/` with restricted permissions (700) to avoid repeated logins; not plaintext credentials
- **Network**: credentials are used only to authenticate with Garmin Connect and are not transmitted to any third-party service; HTML dashboards load Chart.js from `cdn.jsdelivr.net` (pinned versions) — no other external endpoints
- Open source — audit the code yourself

## 📚 Documentation

- **[SKILL.md](SKILL.md)** - Complete Clawdbot setup, commands, troubleshooting
- **[references/health_analysis.md](references/health_analysis.md)** - Science-backed metric interpretation
- **[references/api.md](references/api.md)** - Garmin Connect API details
- **[references/mcp_setup.md](references/mcp_setup.md)** - Claude Desktop MCP setup

## 🐛 Troubleshooting

**Authentication issues?**
- Run `python3 scripts/garmin_auth.py login` to refresh tokens
- Check that `GARMIN_EMAIL` and `GARMIN_PASSWORD` environment variables are set correctly

**No sprints detected?**
- Activity may not include speed data, or you used a non-GPS mode

**Activities not classified?**
- Name your activities with keywords like "game vs X" or "practice"

## 🙏 Credits

- **Author**: Evelyn & Claude
- **Version**: 1.1.3
- **License**: MIT
- **Dependencies**: [python-garminconnect](https://github.com/cyberjunky/python-garminconnect), fitparse, gpxpy

## 🔗 Links

- **GitHub**: [github.com/EvelynDevelops/garmin-frisbee-analysis](https://github.com/EvelynDevelops/garmin-frisbee-analysis)
- **Clawdbot**: [clawdbot.com](https://clawdbot.com)
- **ClawdHub**: [clawdhub.com](https://clawdhub.com)
- **Garmin Connect**: [connect.garmin.com](https://connect.garmin.com)

---

**Questions?** Open an issue on [GitHub](https://github.com/EvelynDevelops/garmin-frisbee-analysis/issues)!
