## Description:

Apollo Mode lets users turn an engineer-mode workflow on or off so an agent clarifies goals, drafts specs, breaks coding work into tasks, checks risks, executes, and verifies outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to activate a lightweight coding-task workflow with objective clarification, specification, planning, risk review, execution, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change how an agent handles coding tasks until it is disabled.

Mitigation: Enable it only when the workflow is wanted, check status when behavior is unclear, and disable the mode when returning to normal interaction.

Risk: Mixed-language command phrases and mode naming may make activation state less clear.

Mitigation: Use explicit enable, disable, and status commands and require short confirmation after state changes.

## Reference(s):

- [Apollo Mode ClawHub page](https://clawhub.ai/nic-yuan/skills/apollo-mode)
- [Plan template](references/plan-template.md)
- [Spec template](references/spec-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or read a small mode state file when the user enables, disables, or checks status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
