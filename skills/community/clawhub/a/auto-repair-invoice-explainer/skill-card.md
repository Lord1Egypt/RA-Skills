## Description:

Breaks down a US auto repair invoice into labor, parts, fees and taxes with plain-language explanations for customers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External customers and service advisors at U.S. independent auto repair shops use this skill to explain invoice items and identify questions for shop clarification. The bundled script currently produces a Markdown lint report rather than the promised invoice breakdown, so its output should not be treated as an explanation or charge validation.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled script performs limited text checks and does not deliver the promised invoice breakdown or validate charges.

Mitigation: Treat its report as a text-checking aid only; prepare and manually review any customer-facing explanation separately.

Risk: Invoice content may include personal details, and explanations may mislead customers if not reviewed.

Mitigation: Omit unnecessary personal data and vehicle identifiers, and review customer-facing explanations manually.

Risk: The script replaces `lint-report.md` in its output folder.

Mitigation: Choose an output folder where replacing that file is acceptable.

Risk: The optional Windows toolkit is a separate unsigned download and is not required by the bundled workflow.

Mitigation: Assess the optional app separately, verify its published hash before running it, and avoid administrator privileges unless necessary.

## Reference(s):

- [US auto repair invoice basics](references/auto-repair-invoice.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/auto-repair-invoice-explainer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain-language invoice explanation guidance; the bundled script writes a Markdown lint report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script checks for required invoice sections, long lines, and banned phrases; it does not produce or validate an invoice breakdown.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
