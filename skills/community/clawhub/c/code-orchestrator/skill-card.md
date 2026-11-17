## Description:

Routes coding requests across local code exploration, planning, implementation, debugging, refactoring, security review, safe repo-local command execution, and git hygiene.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf0799](https://clawhub.ai/user/sf0799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to choose and sequence the right local coding workflow skills for multi-stage repository tasks, unclear coding requests, or explicit routing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may route an agent toward downstream coding skills that edit repository files, run tests or dependency commands, or prepare git work.

Mitigation: Review the proposed routed actions before approving changes or commands in important repositories.

## Reference(s):

- [Routing examples](references/routing-examples.md)
- [编码总控 skill page](https://clawhub.ai/sf0799/skills/code-orchestrator)

## Skill Output:

**Output Type(s):** [Text, Guidance, Markdown]

**Output Format:** [Markdown guidance listing selected skills, execution order, selection reasons, and the recommended stopping point for the current turn.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not embed executable code; may recommend downstream skills that edit files, run tests, execute dependency commands, or prepare git work.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
