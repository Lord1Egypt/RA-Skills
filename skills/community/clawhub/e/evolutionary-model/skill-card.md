## Description:

Framework for building AI agents that evolve with their owner through persistent memory, reusable skills, and operating protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[borodich](https://clawhub.ai/user/borodich)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to set up, explain, or audit a file-based agent framework that evolves through memory, skills, and protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and chat-log files may retain sensitive user or organizational information without clear consent, retention, or deletion controls.

Mitigation: Decide what may be logged before use, minimize or disable raw chat logs, keep memory files out of shared repositories and backups, and define retention and deletion rules.

Risk: Self-modifying agent rules, policy files, or auto-activated skills can change future agent behavior without adequate review.

Mitigation: Require explicit review before changes to AGENTS.md, SOUL.md, policy.yaml, or auto-activated skills are accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/borodich/skills/evolutionary-model)
- [ClawHub publisher profile](https://clawhub.ai/user/borodich)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with file-layout examples and checklist-style steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file names, directory layouts, and policy or memory recommendations; no API calls or commands are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
