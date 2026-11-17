## Description:

Security monitoring and alerting tool for AI agents that checks for exposed secrets, unverified skills, insecure keys, suspicious commands, and malicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suzxclaw](https://clawhub.ai/user/suzxclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers and security-focused agent operators use this skill to scan local OpenClaw agent environments for exposed secrets, insecure SSH keys, unverified skills, suspicious command history, sensitive log data, and supply-chain warning signs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect sensitive local files, SSH key metadata, recent shell history, and OpenClaw logs.

Mitigation: Run it only in environments where that local inspection is acceptable and review generated alerts before acting on them.

Risk: Server security guidance says not to rely on the config file to disable sensitive checks without fixing the script first.

Mitigation: Review the script and confirm enabled checks match the intended environment before installation or scheduled use.

Risk: The server security verdict is suspicious because the skill reads sensitive local files more broadly than its permissions and controls clearly support.

Mitigation: Install only after code review, keep execution scoped to a dedicated OpenClaw workspace, and monitor the local log outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suzxclaw/skills/agent-security-monitor)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal output with local log files and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes scan results to local security-monitor.log and security-alerts.log files.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, README.md version history, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
