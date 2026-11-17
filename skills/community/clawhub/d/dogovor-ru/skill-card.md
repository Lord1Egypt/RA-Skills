## Description:

Dogovor Ru analyzes Russian-language contracts in plain language and highlights key terms, missing information, and risky clauses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggel008](https://clawhub.ai/user/aggel008)

### License/Terms of Use:


## Use Case:

External users can use this skill to review Russian contracts or contract excerpts before signing, understand the main obligations, and identify clauses that may need clarification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run Python and write a persistent local counter unrelated to contract analysis.

Mitigation: Remove or disable the local state tracking before installation, or run the skill only where local command execution and workspace writes are explicitly acceptable.

Risk: The skill may append promotional links to user-facing contract analysis responses.

Mitigation: Remove the promotional attribution behavior or make it clearly acceptable under the deployment environment's user communication policy.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown text with structured contract analysis sections and, in the attribution behavior, inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The user-facing response is a structured plain-language contract review; security evidence notes unrelated local state tracking and promotional link insertion.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
