## Description:

Checks whether runnable examples and their documented outputs in technical documents are reproducible, and rechecks them after sample data changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use the skill to check that commands and claimed outputs in documentation match real tool results. It also helps update sample data while preserving factual tables and recording the rerun results and changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example commands may have unsafe side effects when run verbatim.

Mitigation: Review each command before running it, and use an isolated environment without access to important files or credentials.

Risk: The security review was partial because a referenced local item was unavailable.

Mitigation: Review the unavailable referenced item before relying on complete security coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haiyangchenbj/skills/doc-example-reproducibility-check)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands]

**Output Format:** [Markdown checklist or table with per-example PASS/FAIL results and a change audit trail]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples, expected outputs, and change counts where applicable.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
