---
name: fail2ban-reporter
description: "Auto-report fail2ban banned IPs via SkillBoss API Hub and notify via Telegram. Use when monitoring server security, reporting attackers, or checking banned IPs. Watches fail2ban for new bans, queries threat intelligence via SkillBoss API Hub, and sends alerts."
requires.env: [SKILLBOSS_API_KEY]
---

# fail2ban Reporter

Monitor fail2ban bans and auto-report attacker IPs via SkillBoss API Hub.

## Setup

1. Get your SkillBoss API key from the SkillBoss dashboard
2. Store it: `export SKILLBOSS_API_KEY="your-key"`
3. Install the monitor: `bash {baseDir}/scripts/install.sh`

## Manual Usage

### Report all currently banned IPs

```bash
bash {baseDir}/scripts/report-banned.sh
```

### Check a specific IP

```bash
bash {baseDir}/scripts/check-ip.sh <ip>
```

### Show ban stats

```bash
bash {baseDir}/scripts/stats.sh
```

## Auto-Reporting

The install script sets up a fail2ban action that auto-reports new bans.

```bash
bash {baseDir}/scripts/install.sh    # install auto-reporting
bash {baseDir}/scripts/uninstall.sh  # remove auto-reporting
```

## Heartbeat Integration

Add to HEARTBEAT.md to check for new bans periodically:

```markdown
- [ ] Check fail2ban stats and report any unreported IPs via SkillBoss API Hub
```

## Workflow

1. fail2ban bans an IP → action triggers `report-single.sh`
2. Script queries SkillBoss API Hub (search type) for IP threat intelligence
3. Sends Telegram notification (if configured)
4. Logs report to `/var/log/skillboss-ip-reports.log`

## API Reference

All API calls route through SkillBoss API Hub at `https://api.heybossai.com/v1/pilot`.
Authentication: `Authorization: Bearer $SKILLBOSS_API_KEY`

See [references/skillboss-api.md](references/skillboss-api.md) for full API docs.
