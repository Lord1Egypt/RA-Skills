## Description:

Part of the Overpowered skill suite, this skill helps pressure-test a rule, decision table, SOP, requirement, or business process by finding material edge cases and alternative branches that could break a happy-path specification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill before automation or formalization to identify material non-happy paths, unresolved policy branches, and exception cases that can change process behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect task-relevant workspace artifacts to resolve discoverable facts before asking the user.

Mitigation: Use it in workspaces where the available artifacts are appropriate for process review, and review the resulting exception table before using it for automation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raguets/skills/find-the-exceptions)
- [Overpowered suite](https://github.com/raguets/overpowered)
- [Exception Lenses](artifact/references/exception-lenses.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table with concise summary bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on material exceptions and marks unresolved branches as unknown rather than inventing policy.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
