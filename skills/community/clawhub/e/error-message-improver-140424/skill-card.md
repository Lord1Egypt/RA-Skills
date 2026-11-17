## Description:

Helps developers, support teams, and SaaS operators rewrite unclear error messages so they explain what failed, why it failed, and what to do next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, SaaS operators, and users use this skill to turn vague application errors into actionable messages, templates, checklists, workflows, or implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-invocation wording may cause the skill to activate on general debugging or support requests outside error-message improvement.

Mitigation: Prefer explicit invocation for error-message work and verify that the generated output matches the user's immediate troubleshooting context.

Risk: Generated error-message rewrites or workflows could omit important diagnostic detail or suggest an inaccurate next action.

Mitigation: Review the result against the stated success criteria, confirm assumptions with the application owner when needed, and test proposed messages or changes before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-140424)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, checklist, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no privileged tools or external services are required by the skill itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
