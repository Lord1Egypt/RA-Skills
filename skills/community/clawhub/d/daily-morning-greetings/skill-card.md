## Description:

This skill generates fixed-format daily Chinese morning greetings with live weather, rotating icons, local wisdom-and-blessing pairs, alternate variants, and optional OpenClaw schedule or Weixin bot delivery support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joannaxing](https://clawhub.ai/user/joannaxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to generate or schedule concise daily morning greetings that combine current weather, clothing guidance, and a rotating wisdom quote. It also supports manual reruns, alternate greeting variants, and optional Weixin bot fanout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Weixin fanout can send the generated greeting to webhook URLs detected from environment variables or OpenClaw configuration.

Mitigation: Review WEIXIN/WECHAT webhook variables and OpenClaw configuration before installation, and keep Weixin fanout disabled unless that delivery path is intended.

Risk: Live weather and geocoding lookups contact external weather services and may include the configured city or coordinates.

Mitigation: Use explicit, non-sensitive location settings and confirm that network access to weather services is acceptable for the deployment environment.

Risk: Scheduled delivery can post greetings to an unintended chat or route if cron delivery settings are wrong.

Mitigation: Confirm the delivery route when creating or updating schedules, and use failure alerts that follow the same intended channel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joannaxing/skills/daily-morning-greetings)
- [Publisher Profile](https://clawhub.ai/user/joannaxing)
- [wisdom_pairs.json](references/wisdom_pairs.json)
- [Publisher Homepage](https://iheaven.org)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [wttr.in Weather Service](https://wttr.in)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default location is Shanghai; live weather requires network access; optional Weixin fanout may send the generated greeting to a configured webhook.]

## Skill Version(s):

1.0.12 (source: evidence.release.version, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
