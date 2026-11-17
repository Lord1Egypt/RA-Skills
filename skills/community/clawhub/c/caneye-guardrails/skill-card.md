## Description:

Checks your canEYE rules before this agent sends, buys, books, shares, deletes, cancels, pays, connects a new tool or uses saved keys for you, and waits for your okay in canEYE when a rule says "Ask me".

This skill is ready for commercial/non-commercial use.

## Publisher:

[mckenzie1975](https://clawhub.ai/user/mckenzie1975)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to check their canEYE rules before an agent takes covered actions on their behalf. It helps the agent follow automatic, ask-first, and never decisions, including waiting for approval when required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses shell capability without a declared tool scope.

Mitigation: Before installing, consider whether this level of shell access is appropriate for your environment.

Risk: The security scan evidence is incomplete because one reference could not be resolved.

Mitigation: Review the unresolved reference and the skill before relying on the scan result.

## Reference(s):

- [canEYE](https://caneye.ai)
- [canEYE actions](references/categories.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands]

**Output Format:** [JSON decisions with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action summaries and relevant amount, target, or resource details; message, file, and email contents are not sent.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
