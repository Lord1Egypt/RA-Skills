## Description:

Generate daily morning briefings with weather, traffic limits, and news. Provides structured data collection scripts for stable, reproducible briefing generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to generate recurring daily briefings for Beijing-oriented weather, traffic restrictions, and current news. It supports human-readable briefing output and structured JSON for downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A city name can reach local command execution in the weather lookup path.

Mitigation: Use only trusted city values until the shell-based weather fetch is replaced with safe HTTP fetching.

Risk: The README includes a recurring email example addressed to a fixed third-party address.

Mitigation: Change the recipient to an address you control and require explicit approval before enabling scheduled delivery.

Risk: The Beijing traffic restriction rules are hard-coded for 2025-12-29 through 2026-03-29 and are stale as of 2026-09-16.

Mitigation: Update the traffic rule table from an authoritative source before relying on traffic restriction output.

Risk: Briefing content depends on live weather and news sources that can fail, change format, or return incomplete data.

Mitigation: Review generated briefings before distribution and monitor source failures, cached fallbacks, and stale data indicators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoyachao/skills/dailybriefing)
- [Node.js](https://nodejs.org/)
- [wttr.in weather service](https://wttr.in/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown briefing text or JSON, with shell commands and cron configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output can vary by date, city option, cached data, and live weather or news source availability.]

## Skill Version(s):

1.0.0 (source: server release metadata and manifest.yaml; artifact changelog/package.json disagree)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
