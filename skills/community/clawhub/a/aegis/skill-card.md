## Description: <br>
Automated Emergency Geopolitical Intelligence System - real-time threat monitoring and safety alerts for civilians in conflict zones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PleaseChooseUsername](https://clawhub.ai/user/PleaseChooseUsername) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use AEGIS to configure location-aware crisis monitoring, run manual or scheduled scans, receive Telegram alerts for critical threats, and generate morning or evening safety briefings. It is intended for civilian emergency awareness and preparedness in conflict-zone or regional-security scenarios. <br>

### Deployment Geography for Use: <br>
Global, with packaged country-profile evidence currently focused on the UAE. <br>

## Known Risks and Mitigations: <br>
Risk: Automated crisis alerts can influence urgent safety decisions and may be wrong, stale, or incomplete. <br>
Mitigation: Test scans manually before enabling cron and verify urgent alerts against official emergency, government, and embassy sources before acting. <br>
Risk: Telegram bot credentials and local AEGIS configuration/state files can expose channel access or sensitive location context. <br>
Mitigation: Use a dedicated low-privilege Telegram bot, protect ~/.openclaw files, and avoid showing configuration or logs during screen sharing. <br>
Risk: Optional cloud LLM verification can send sensitive crisis or location context to a third-party endpoint. <br>
Mitigation: Prefer local Ollama for sensitive deployments, or disable LLM verification when external sharing is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PleaseChooseUsername/aegis) <br>
- [Project homepage](https://github.com/PleaseChooseUsername/aegis-openclaw-skill) <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Source Registry](references/source-registry.json) <br>
- [Threat Keywords](references/threat-keywords.json) <br>
- [UAE Country Profile](references/country-profiles/uae.json) <br>
- [Go-Bag Checklist](references/preparedness/go-bag-checklist.md) <br>
- [Communication Plan](references/preparedness/communication-plan.md) <br>
- [Shelter Guidance](references/preparedness/shelter-guidance.md) <br>
- [Evacuation Guidance](references/preparedness/evacuation-guidance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets; runtime scripts emit JSON, logs, Telegram messages, and briefing text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write local OpenClaw state files and post to Telegram when credentials and channel delivery are configured.] <br>

## Skill Version(s): <br>
3.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
