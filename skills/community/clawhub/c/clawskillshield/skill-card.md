## Description:

ClawSkillShield locally scans OpenClaw and ClawHub skills for security risks such as hardcoded secrets, dangerous calls, risky imports, obfuscation, and hardcoded IP addresses, then returns a scored threat report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abyousef739](https://clawhub.ai/user/abyousef739)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use ClawSkillShield to scan local OpenClaw or ClawHub skill folders before installation and to generate reviewable risk reports. Its quarantine action can move a skill directory, so it should be reserved for confirmed high-risk cases with human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads files under paths provided by the caller.

Mitigation: Run it only against intended skill directories and avoid pointing it at unrelated sensitive local folders.

Risk: The quarantine action can move local directories and replace an existing quarantine target with the same basename.

Mitigation: Require human approval before quarantine, verify the path is the intended skill directory, and keep backups of important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abyousef739/skills/clawskillshield)
- [Publisher profile](https://clawhub.ai/user/abyousef739)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown-style security reports with CLI status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scans local paths supplied by the caller; quarantine moves a target directory into the local OpenClaw quarantine folder.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; package metadata reports 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
