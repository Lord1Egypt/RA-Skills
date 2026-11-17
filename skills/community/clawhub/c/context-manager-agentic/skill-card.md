## Description:

Verifies and distributes trust-gated memory and skill-file context to a multi-agent roster before it is injected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tryboy869](https://clawhub.ai/user/tryboy869)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to prepare scoped, trust-gated context bundles for multiple agents and to detect modified memory or skill files before they are treated as instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation depends on mutable external code that was not included for review.

Mitigation: Review the referenced GitHub repository and npm dependency tree before installing, prefer a pinned commit or signed release with a lockfile, and run installation in a sandbox with only required files and credentials.

Risk: Unverified memory or skill files could affect agent behavior if treated as trusted instructions.

Mitigation: Use manifest review and hash verification before distribution, and keep untrusted content tagged as reference material rather than executable instruction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tryboy869/skills/context-manager-agentic)
- [Context Manager Agentic GitHub Repository](https://github.com/Tryboy869/context-manager-agentic)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Context distribution output separates team-shared context from role-specific context and tags untrusted content as reference material.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
