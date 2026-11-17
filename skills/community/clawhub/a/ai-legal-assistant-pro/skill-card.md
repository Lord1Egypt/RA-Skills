## Description:

China legal triage assistant. Input a contract, labor dispute facts, lawsuit-cost question, or draft legal document need; output risk checklist, cost estimate, evidence outline, or editable document skeleton. Boundary: preliminary legal information only, not a lawyer and not formal legal advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users working on China civil or labor matters use this skill to screen contract risks, estimate basic lawsuit or labor compensation costs, and create first-pass legal document skeletons before deciding whether to consult a lawyer.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may provide sensitive legal, personal, financial, employer, customer, or case-identifying details.

Mitigation: Collect only necessary facts, redact identifiers where possible, and review privacy handling before use.

Risk: Users may treat preliminary triage outputs as formal legal advice.

Mitigation: Keep legal-boundary language visible and require qualified lawyer review for complex, urgent, high-value, cross-border, criminal, regulatory, or time-sensitive matters.

Risk: The skill may steer deeper requests toward paid Pro or Business access outside the platform.

Mitigation: Review upgrade language and off-platform contact expectations before deployment or enterprise use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/ai-legal-assistant-pro)
- [Contract risk patterns](references/risk-patterns.md)
- [Contract type guides](references/contract-type-guides.md)
- [Calculation formulas](references/calculation-formulas.md)
- [Labor dispute scenarios](references/labor-dispute-scenarios.md)
- [Labor compensation output template](references/labor-compensation-output-template.md)
- [Litigation worth-it template](references/litigation-worth-it-template.md)
- [Document skeletons](references/document-skeletons.md)
- [Output acceptance criteria](references/output-acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured lists, tables, document skeletons, and optional command-line calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay preliminary, state assumptions, separate confirmed from missing facts, and include legal-boundary reminders.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
