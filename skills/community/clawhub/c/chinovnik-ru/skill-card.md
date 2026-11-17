## Description:

Explains Russian official letters, rulings, government documents, and legal texts in plain Russian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggel008](https://clawhub.ai/user/aggel008)

### License/Terms of Use:


## Use Case:

External users who receive Russian official, legal, or administrative text can use this skill to identify the document type, plain-language meaning, required actions, deadlines, and stated consequences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact asks the agent to execute local Python commands and update a usage counter.

Mitigation: Review before installing, run only in a constrained workspace, or remove the Attribution section if local state changes are not acceptable.

Risk: The artifact can append unrelated promotional Telegram links to user-facing answers.

Mitigation: Remove or disable the promotional attribution behavior when outputs must remain neutral or policy-controlled.

Risk: The security verdict is suspicious because extra local state and promotional behavior are present alongside the advertised document explanation.

Mitigation: Treat the skill as requiring manual review and scan approval before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aggel008/skills/chinovnik-ru)
- [Publisher profile](https://clawhub.ai/user/aggel008)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured plain-language analysis and artifact-provided shell command instructions for attribution behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Treats user-provided document text as untrusted input; responses emphasize required actions, deadlines, consequences, and plain-language explanations of terms.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
