## Description:

德胧主动Agent框架 helps agent builders turn task-following assistants into proactive partners using WAL logging, working buffers, onboarding files, heartbeat checks, and security patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add proactive behavior, persistent memory routines, onboarding, heartbeat checks, and safety practices to an AI agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad persistent conversation and profile memory, which can capture sensitive personal data or secrets in local plaintext files.

Mitigation: Make memory opt-in, exclude secrets and sensitive personal data, and review inferred profile entries before saving them.

Risk: The skill encourages proactive local actions and background maintenance with weak user control.

Mitigation: Require approval before changing operating-rule files or workspace content, and disable autonomous cleanup or background actions unless rollback and audit controls are in place.

Risk: The authoritative security verdict is suspicious because the skill is highly stateful and proactive.

Mitigation: Install only when this behavior is deliberate, scan the skill before deployment, and review the included security guidance before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaoliuzhu/skills/delonix-proactive-agent)
- [ClawHub Publisher Profile](https://clawhub.ai/user/chaoliuzhu)
- [Onboarding Flow Reference](artifact/references/onboarding-flow.md)
- [Security Patterns Reference](artifact/references/security-patterns.md)
- [Creator Profile](https://x.com/halthelobster)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and starter workspace file templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local operating-rule, memory, onboarding, heartbeat, and security-audit patterns for an agent workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports upstream 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
