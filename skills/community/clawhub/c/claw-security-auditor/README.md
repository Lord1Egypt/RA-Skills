# Security Auditor — OpenClaw Skill

Autonomously scans all installed OpenClaw skills for security risks using
static analysis. No skill code is ever executed.

## Installation

```bash
# Copy to your OpenClaw skills directory
cp -r security-auditor ~/.openclaw/skills/security-auditor

# Or for workspace-local use
cp -r security-auditor ./skills/security-auditor
```

## Dashboard (GUI)

Run the local web dashboard for a visual risk overview:

```bash
node scripts/dashboard.js
# or point at a specific skills directory:
node scripts/dashboard.js --dir data/sample-skills
# custom port:
node scripts/dashboard.js --port 8080
# skip auto-opening the browser:
node scripts/dashboard.js --no-open
```

Opens `http://localhost:7777` automatically. No build step, no npm install — pure Node.js stdlib on the server, vanilla JS in the browser.

Features:
- Live risk summary (total / high / medium / low counts)
- Expandable skill cards with score ring, triggered rules, threats, simulation, recommendations
- Trust score bar per skill
- Filter by risk level, search by name or behavior
- Whitelist toggle directly from the UI (re-scans automatically)



Once installed, just ask your agent:

```
"Audit all my installed skills"
"Are my skills safe?"
"Run a security scan on the file-cleaner skill"
"Give me a security report"
```

## Usage via CLI (direct)

```bash
# Scan all skills (default paths)
node scripts/audit.js

# Scan a specific directory of skills
node scripts/audit.js --dir data/sample-skills

# Scan a single skill by name
node scripts/audit.js --dir data/sample-skills --skill file-cleaner

# Output formats
node scripts/audit.js --dir data/sample-skills --output json      # machine-readable
node scripts/audit.js --dir data/sample-skills --output markdown  # Markdown report
node scripts/audit.js --dir data/sample-skills --output csv       # CSV export

# Filter by severity
node scripts/audit.js --severity high     # only High risk skills
node scripts/audit.js --severity medium   # only Medium risk skills

# Save report to ~/.openclaw/security-reports/
node scripts/audit.js --dir data/sample-skills --save

# Compare against last saved report (shows what changed)
node scripts/audit.js --dir data/sample-skills --compare

# Auto-generate patched SKILL.md with dangerous permissions stripped
node scripts/audit.js --dir data/sample-skills --fix

# Show trust score history for all skills
node scripts/audit.js --trust

# Show rule-frequency analytics
node scripts/audit.js --dir data/sample-skills --stats

# Manage the whitelist
node scripts/whitelist.js add weather-lookup
node scripts/whitelist.js list
node scripts/whitelist.js remove weather-lookup

# Continuous monitoring (background watcher)
node scripts/monitor.js
node scripts/monitor.js --alert-only   # only print on High risk

# Run the test suite
node scripts/test.js
```

## Testing with sample skills

```bash
node scripts/audit.js --dir data/sample-skills
```

> **Note:** `data/sample-skills/` contains intentionally risky demo scripts used
> to validate the auditor's detection rules. They are not needed for normal use
> and can be safely deleted if you do not want potentially dangerous demo code on disk:
> ```bash
> rm -rf data/sample-skills
> ```

See `data/example-output.md` for expected output against the three sample skills.

## Continuous monitoring (optional, advanced)

> ⚠️ **This is an optional feature.** Running the monitor as a background service
> means it will continuously read skill files and run on every login. Only enable
> this if you have reviewed the code and are comfortable with that behavior.

Run the monitor script in the background to auto-audit whenever a skill file changes:

```bash
node scripts/monitor.js
# or, only alert on High risk findings:
node scripts/monitor.js --alert-only
```

If you choose to run it automatically on login, the recipes below show how.
**Review the code first and only proceed if you trust the package source.**

**launchd (macOS)** — create `~/Library/LaunchAgents/com.openclaw.security-monitor.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.openclaw.security-monitor</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/node</string>
    <string>/path/to/security-auditor/scripts/monitor.js</string>
    <string>--alert-only</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/tmp/openclaw-monitor.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/openclaw-monitor.log</string>
</dict>
</plist>
```
Then: `launchctl load ~/Library/LaunchAgents/com.openclaw.security-monitor.plist`

**systemd (Linux)** — create `~/.config/systemd/user/openclaw-monitor.service`:
```ini
[Unit]
Description=OpenClaw Security Monitor

[Service]
ExecStart=/usr/bin/node /path/to/security-auditor/scripts/monitor.js --alert-only
Restart=on-failure

[Install]
WantedBy=default.target
```
Then: `systemctl --user enable --now openclaw-monitor`

## Risk scoring

| Score | Level  | Meaning                                      |
|-------|--------|----------------------------------------------|
| 0–29  | 🟢 Low  | Benign — review optional                    |
| 30–59 | 🟡 Medium | Warrants manual review before trusting    |
| 60+   | 🔴 High | Disable or sandbox immediately              |

H2 (remote code execute) or H4 (obfuscation) always forces High regardless of score.

## Architecture

```
security-auditor/
├── SKILL.md                    ← Agent instructions + metadata
├── README.md                   ← This file
├── scripts/
│   ├── audit.js                ← Core analysis engine (static analysis)
│   ├── dashboard.js            ← Local web dashboard server
│   ├── whitelist.js            ← Whitelist manager
│   ├── monitor.js              ← Continuous file watcher
│   └── test.js                 ← Self-test suite
├── ui/
│   └── index.html              ← Dashboard UI (self-contained, no build step)
└── data/
    ├── example-output.md       ← Sample report output
    └── sample-skills/          ← Demo skills for testing
        ├── file-cleaner/       ← High risk example
        ├── data-sync/          ← Medium risk example
        └── weather-lookup/     ← Low risk (clean) example
```

## Detection rules (v3)

44 rules across 3 risk levels:

High risk (H1–H16): shell execution, remote code download, file deletion, obfuscation, privilege escalation, credential harvesting, .env access, keyloggers, clipboard theft, screen capture, crypto mining, reverse shells, registry manipulation, persistence mechanisms, SQL/command injection, supply-chain/runtime package install

Medium risk (M1–M20): network calls, sensitive directory access, data exfiltration, dynamic eval, permission mismatch, unscoped writes, DoS patterns, browser storage, WebSocket C2, DNS lookups, process enumeration, network enumeration, file archiving/staging, timing evasion, self-modification, cloud IMDS access, prototype pollution, path traversal, unsafe deserialization, hardcoded credentials

Low risk (L1–L10): telemetry, third-party APIs, env var reads, sparse docs, hardcoded URLs, security TODOs, weak crypto, insecure HTTP, debug artifacts, large file anomaly

Plus: Shannon entropy analysis (H4e) — detects high-entropy strings that may be embedded secrets or encoded payloads

## New features (v2/v3)

- `--dir <path>` — scan any directory of skills
- `--output markdown` — Markdown report
- `--output csv` — CSV export (one row per skill, importable into spreadsheets)
- `--compare` — diff current scan against last saved report
- `--fix` — auto-generate `SKILL.patched.md` with dangerous permissions stripped
- `--trust` — display trust score history with trend indicators
- `--stats` — rule-frequency analytics: which rules fire most, average risk score
- `--severity high|medium|low` — filter output to one risk level
- Shannon entropy analysis (H4e) — catches embedded secrets/payloads not caught by base64 patterns
- Rules H15–H16 — SQL/command injection, supply-chain/runtime package install
- Rules M17–M20 — prototype pollution, path traversal, unsafe deserialization, hardcoded credentials
- `scoreBreakdown` field in JSON output — per-rule score contribution
- Dashboard: Stats tab with rule-frequency bar chart
- Dashboard: Score breakdown section per skill card
- Dashboard: Risk trend sparkline on each card (from trust history)
- Dashboard: CSV export button (⬇ CSV in header)
- Dashboard: `R` keyboard shortcut to rescan
- Dashboard: Search now matches rule IDs and labels too
- Dashboard: `POST /api/scan/single` — re-scan one skill by name
- Dashboard: `GET /api/stats` — rule frequency analytics endpoint
- Dashboard: `GET /api/export/csv` — CSV download endpoint

## Constraints

- Static analysis only — no skill code is ever executed
- Read-only — never modifies or deletes skill files
- No external dependencies — pure Node.js stdlib
