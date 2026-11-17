## Description:

Brainstorm Council runs a multi-role adversarial brainstorm in which four conflicting expert personas interview the user, test tradeoffs, defend recommendations, and hand off to a fifth role for a standalone planning report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bystry95](https://clawhub.ai/user/bystry95)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and planners use this skill to structure decisions with competing tradeoffs, surface conflicting expert perspectives, ask targeted follow-up questions, and produce a standalone action report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Planning recommendations may be incomplete or incorrect when the user skips questions or supplies uncertain information.

Mitigation: Review the final report before acting and treat unanswered questions as decision gaps, especially for legal, financial, safety, or operational choices.

Risk: The adversarial format can produce forceful tradeoff recommendations that are useful for planning but are not a substitute for qualified professional review.

Mitigation: Use the report to identify options, risks, and next steps, then validate high-impact decisions with appropriate stakeholders or specialists.

Risk: The expected behavior is chat-only; unexpected file writes, network access, credential requests, or system changes would fall outside the reviewed behavior.

Mitigation: Stop execution and re-review the skill if an agent attempts to modify files, access external systems, or request secrets while using this skill.

## Reference(s):

- [Role construction and phase templates](references/roles-and-templates.md)
- [ClawHub skill page](https://clawhub.ai/bystry95/skills/brainstorm-council)
- [ClawHub publisher profile](https://clawhub.ai/user/bystry95)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style chat response with debate notes followed by a standalone report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat-only output; the skill instructs the agent not to write files and to stay within a 15-call budget.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
