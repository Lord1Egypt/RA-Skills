## Description:

Ctct Security Patrol helps OpenClaw and TeleClaw users run local security audits, inspect host and skill state, optionally configure OpenClaw cron checks, and optionally upload audit summaries to Changeway's threat-intelligence service with explicit consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsyjx0115](https://clawhub.ai/user/zsyjx0115)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators who use OpenClaw or TeleClaw use this skill to run security patrols, inspect local configuration and skill inventory, review summarized audit results, and optionally set up recurring local checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad local host inspection and persists reports and security baselines.

Mitigation: Install and run it only in environments where local host inspection is expected, and review the generated files under the OpenClaw state directory before sharing them.

Risk: Using --push sends privacy-sensitive device and skill inventory data to auth.ctct.cn.

Mitigation: Use local mode by default, require explicit user consent for --push, and avoid --push unless the user trusts the Changeway-operated endpoint.

Risk: Server security evidence says the offline-mode agent_id behavior conflicts with the skill's privacy claim.

Mitigation: Fix or verify the agent_id creation behavior before treating local mode as privacy-preserving.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsyjx0115/skills/ctct-security-patrol)
- [Cron setup guide](references/cron-setup.md)
- [Changeway audit upload endpoint](https://auth.ctct.cn:10020/changeway-open/api/pushAuditData)
- [Changeway skill assessment endpoint](https://auth.ctct.cn:10020/changeway-open/api/skills/assessment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and summarized audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the audit script is executed, it writes local text and JSON reports plus baseline files under the user's OpenClaw state directory.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
