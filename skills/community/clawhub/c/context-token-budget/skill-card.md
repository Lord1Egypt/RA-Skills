## Description:

Estimates token use for text or a local file and checks it against a configurable budget, returning a PASS/FAIL verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and other agent users can check the estimated size of text or a local file before adding it to an AI context, and decide whether to trim it or raise the budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Estimated counts may differ from the target model's actual tokenization.

Mitigation: Treat results as rough estimates; confirm tight limits with the target model's tokenizer and leave a margin.

Risk: A user-specified file may contain sensitive text that the checker reads locally.

Mitigation: Supply only intended files or text, and review the input before running the command.

Risk: Broad activation terms may invoke the budget check unintentionally.

Mitigation: Narrow activation terms if unrequested checks disrupt the workflow.

## Reference(s):

- [Context Token Budget on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/context-token-budget)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimated tokens, budget, usage percentage, PASS/FAIL verdict, a SHA-256 prefix, and advice; an over-budget result exits with code 1.]

## Skill Version(s):

1.0.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
