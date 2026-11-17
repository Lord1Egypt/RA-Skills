## Description:

Plant decoy credentials in your OpenClaw workspace to detect malicious skill behavior. Canary tokens trigger alerts when read, copied, or exfiltrated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users can plant fake credentials to detect when a skill or agent accesses them, then review alerts and remove the canaries when they are no longer needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canary deployment may overwrite an existing credential backup, causing data loss.

Mitigation: Inspect the target paths before deployment and preserve any existing files; deploy only in the intended workspace.

## Reference(s):

- [Agent Canary on ClawHub](https://clawhub.ai/thomaszhou22/skills/agent-canary)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files, Configuration]

**Output Format:** [Markdown guidance and alerts, shell commands, and JSON or environment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create decoy credential files and incident records in the configured workspace.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
