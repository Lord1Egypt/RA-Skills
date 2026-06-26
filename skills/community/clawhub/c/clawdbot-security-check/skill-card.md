## Description: <br>
Clawdbot Security Check is a knowledge-based audit framework that helps Clawdbot inspect its configuration across security domains and recommend hardening steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit Clawdbot configuration, detect security misconfigurations, and receive prioritized remediation guidance. It is intended for local security hardening workflows where the agent can inspect relevant Clawdbot files and settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as read-only, but the artifact documents a --fix mode that can persistently change bot policy, logging behavior, and file permissions. <br>
Mitigation: Run normal audit commands as read-only, and use --fix only after reviewing the intended changes and backing up affected Clawdbot configuration and state files. <br>
Risk: Audit output may expose token-bearing or sensitive local configuration content. <br>
Mitigation: Limit output sharing, redact credentials before distribution, and run the audit only where local Clawdbot files can be inspected safely. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/TheSethRose/clawdbot-security-check) <br>
- [Official ClawdBot gateway security documentation](https://docs.clawd.bot/gateway/security) <br>
- [Original security framework reference](https://x.com/DanielMiessler/status/2015865548714975475) <br>
- [Artifact-declared project homepage](https://github.com/TheSethRose/Clawdbot-Security-Check) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with audit findings, severity summaries, remediation steps, and inline shell or JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local configuration excerpts or token-bearing output when the agent inspects Clawdbot files.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
