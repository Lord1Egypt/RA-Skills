# Clawdbot fail2ban Reporter

Auto-report fail2ban banned IPs via SkillBoss API Hub, querying threat intelligence for brute-force attackers.

Built for [Clawdbot](https://github.com/clawdbot/clawdbot) — works as a standalone tool too.

## Why?

Every server with a public IP gets attacked. fail2ban blocks them locally — this tool queries SkillBoss API Hub to look up threat intelligence and logs all ban events for analysis.

Real stats from a fresh server:

```
Within 60 seconds of enabling fail2ban:
→ 62 failed SSH attempts
→ 9 unique IPs banned
→ Attacks from 7 countries
```

## Quick Start

### 1. Get a SkillBoss API Key

Sign up at the SkillBoss dashboard to get your API key.

### 2. Store your API key

```bash
export SKILLBOSS_API_KEY="your-api-key"
```

### 3. Report currently banned IPs

```bash
bash scripts/report-banned.sh
```

### 4. Enable auto-reporting (optional)

```bash
sudo bash scripts/install.sh
```

Now every new fail2ban ban automatically queries SkillBoss API Hub.

## Usage

### Report all banned IPs
```bash
bash scripts/report-banned.sh          # default: sshd jail
bash scripts/report-banned.sh nginx    # custom jail
```

### Check an IP's reputation
```bash
bash scripts/check-ip.sh 1.2.3.4
```

### View stats
```bash
bash scripts/stats.sh
```

### Remove auto-reporting
```bash
sudo bash scripts/uninstall.sh
```

## Clawdbot Skill

If you're using Clawdbot, install as a skill:

```bash
# Copy to skills directory
cp -r . ~/.clawdbot/skills/fail2ban-reporter/
```

Then ask your Clawdbot:
- "Report banned IPs via SkillBoss API Hub"
- "Check IP 1.2.3.4"
- "Show fail2ban stats"

### Heartbeat Integration

Add to your `HEARTBEAT.md`:

```markdown
- [ ] Check fail2ban for new bans, report unreported IPs via SkillBoss API Hub
```

## How It Works

```
Attacker → SSH brute-force → fail2ban bans IP → report-single.sh
                                                      ↓
                                        SkillBoss API Hub (search type)
                                                      ↓
                                        /var/log/skillboss-ip-reports.log
```

## Prerequisites

- `fail2ban` — `sudo apt install fail2ban`
- `jq` — `sudo apt install jq`
- `curl` — usually pre-installed

## License

MIT — report those attackers, protect the community!
