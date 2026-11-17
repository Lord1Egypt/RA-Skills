## Description:

Runtime-neutral orchestration: keep this session as decision maker/integrator; for non-trivial work prefer bounded available agents for search, reading, research, testing, review, and mutually exclusive writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[its-how](https://clawhub.ai/user/its-how)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to guide runtime-neutral task orchestration, including capability discovery, bounded delegation, transparency, verification, and re-orchestration when gaps appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upgrade instructions may encourage installing or updating the latest package without reviewing the exact version.

Mitigation: Review the repository state first and prefer a pinned or verified version before running update commands.

Risk: The skill can influence how an agent delegates, reports work, and prepares handoff material.

Mitigation: Keep approval gates, permission limits, secret handling, and explicit confirmation requirements in force when applying orchestration guidance.

## Reference(s):

- [Capability Orchestration](references/capability-orchestration.md)
- [aha-orch repository](https://github.com/its-How/aha-orch)
- [ClawHub skill page](https://clawhub.ai/its-how/skills/aha-orch-xx)
- [Publisher profile](https://clawhub.ai/user/its-how)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No persistent state; output is advisory orchestration guidance for the consuming agent.]

## Skill Version(s):

1.1.0 (source: server release, target metadata, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
