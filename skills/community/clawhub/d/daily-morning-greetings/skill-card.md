## Description: <br>
Generates fixed-format Chinese daily morning greetings with live weather, rotating icons, and wisdom-and-blessing pairs, and can help configure recurring OpenClaw delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joannaxing](https://clawhub.ai/user/joannaxing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who want an automated Chinese morning greeting use this skill to generate or schedule a three-paragraph message with weather and a short wisdom/blessing segment. It supports manual resend or alternate phrasing while defaulting to Shanghai unless a city is specified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring schedules and failure alerts may send messages to the wrong destination if the cron route is misconfigured. <br>
Mitigation: Confirm the cron schedule, primary chat destination, and failure-alert destination before enabling the skill. <br>
Risk: Optional Weixin fanout may post the generated greeting externally using detected webhook credentials. <br>
Mitigation: Allow --deliver-weixin auto only after confirming the intended webhook source and destination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joannaxing/daily-morning-greetings) <br>
- [wisdom_pairs.json](references/wisdom_pairs.json) <br>
- [Project homepage](https://iheaven.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text greeting, JSON context from local scripts, or Markdown with bash code blocks for configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The user-facing greeting is a three-paragraph Chinese message; live weather may be unavailable; optional Weixin webhook fanout can occur when configured.] <br>

## Skill Version(s): <br>
1.0.12 (source: evidence.release.version, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
