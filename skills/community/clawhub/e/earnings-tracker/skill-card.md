## Description:

Scans Chinese A-share earnings calendars and performance forecasts for configured stock watchlists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan earnings-related data for configured stock watchlists and summarize matching Chinese A-share earnings calendar and forecast items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented U.S. market scanning, scheduling, and Discord/Telegram delivery may not work as advertised.

Mitigation: Treat the skill as a Chinese A-share scanner unless reviewed code and tests demonstrate the additional documented integrations.

Risk: The scanner writes persistent output to a fixed OpenClaw memory path without clear user control.

Mitigation: Review and change the output path to an explicit, user-approved location before running the skill in a shared or sensitive environment.

Risk: The skill depends on akshare for market data retrieval.

Mitigation: Pin and review the akshare dependency and run the scanner in an isolated environment before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/earnings-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance, shell commands, console text, and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner uses a configured watchlist and can write earnings scan results to a local JSON file.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
