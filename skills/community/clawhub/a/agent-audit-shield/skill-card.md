## Description:

Agent Audit Shield presents itself as a local command-security auditor for AI agents, scanning commands for data-leak and destructive-file-operation risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add command-risk review around local AI agent activity, especially commands that may expose secrets or destructively modify files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The usage command relies on an unpinned npx-resolved package, so the executed code may differ over time.

Mitigation: Pin the package version, verify the publisher and source, and use integrity or lockfile checks before installation.

Risk: The reviewed artifact claims command-security safeguards but does not include auditable implementation files for those safeguards.

Mitigation: Review the resolved package contents and run it in a sandbox with minimal filesystem and environment access before granting broader permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmstudio667-commits/skills/agent-audit-shield)
- [ClawHub publisher profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown text with inline bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include human-in-the-loop approval guidance for local command execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
