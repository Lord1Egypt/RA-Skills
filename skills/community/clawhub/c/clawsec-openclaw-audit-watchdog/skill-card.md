## Description: <br>
Automates daily OpenClaw security audits by creating or updating a recurring cron job and delivering formatted reports to configured DM and optional email recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and security operators use this skill to schedule recurring OpenClaw security audits, summarize standard and deep audit findings, and deliver reports to configured recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can create an unattended recurring security-audit job and send reports to external DM or email recipients. <br>
Mitigation: Enable it only when recurring audits are intended; verify recipients, schedule, install directory, SMTP/sendmail settings, and how to disable or remove the OpenClaw cron job. <br>
Risk: Broad triggers and limited final confirmation can make accidental activation plausible. <br>
Mitigation: Invoke it by exact skill name, review the preflight details before persistence, and keep required recipient environment variables unset until setup is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-openclaw-audit-watchdog) <br>
- [Skill homepage](https://clawsec.prompt.security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text reports with shell commands and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates an unattended OpenClaw cron job when configured; requires bash, openclaw, node, and DM recipient environment variables.] <br>

## Skill Version(s): <br>
0.1.9 (source: frontmatter, changelog, skill.json, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
