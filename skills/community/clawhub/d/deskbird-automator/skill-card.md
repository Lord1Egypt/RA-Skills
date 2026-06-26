## Description: <br>
Steuert Deskbird ueber Telegram mit sicherem Auth-Handling, Discovery und Parkplatz-Status/Reservierung. Verwende diesen Skill, wenn ein OpenClaw-Agent Deskbird-Aufgaben ausfuehren oder eine wiederkehrende Cron-Session dafuer anlegen/aktualisieren soll, inklusive Rueckfrage zum Rhythmus und Reauth bei abgelaufener Auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geby85](https://clawhub.ai/user/geby85) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and automation operators use this skill to check Deskbird authentication, discover workspace and parking availability, report status through Telegram, and optionally create a recurring OpenClaw cron session for cautious Deskbird monitoring or parking reservation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle live Deskbird session credentials through Telegram and authenticated local tooling. <br>
Mitigation: Install only where the bot, logs, and storage path are trusted; prefer local or scoped authentication and rotate or revoke Deskbird/Firebase credentials when the skill is no longer used. <br>
Risk: Recurring automation can retain Deskbird account authority and perform booking-related actions. <br>
Mitigation: Review each cron prompt before enabling it, keep safe mode active, avoid aggressive retries, and start booking workflows with dry-run before allowing a real reservation. <br>
Risk: Broad authenticated API debugging commands may expose or replay sensitive account data if misused. <br>
Mitigation: Use the documented auth-check, auth-refresh, discovery, parking-status, and parking-book-first flows for normal operation, and reserve capture, probe, replay, or pairing flows for deliberate debugging. <br>


## Reference(s): <br>
- [Cron Session Prompt Template](artifact/references/cron-session-template.md) <br>
- [Deskbird-Automator ClawHub Release](https://clawhub.ai/geby85/deskbird-automator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-capable CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update an OpenClaw cron session prompt and may call local Deskbird CLI commands that return table or JSON output.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
