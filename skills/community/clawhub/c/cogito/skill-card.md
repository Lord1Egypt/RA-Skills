## Description:

Cogito activates a Socratic self-reflection mode that helps users examine assumptions, contradictions, and values in their own words, with optional user-confirmed personalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent use Cogito when they want guided self-reflection rather than advice. The skill prompts users through reflection, contradiction-finding, and thought experiments, and can store user-approved personalization in a local profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The probing reflection style may be inappropriate for therapy, crisis, or high-stakes mental health situations.

Mitigation: Use the skill for self-reflection only, avoid crisis or therapy use, and route urgent safety concerns to appropriate support.

Risk: Evolution can retain conversation-derived personal details in the local user profile.

Mitigation: Approve only profile entries the user is comfortable retaining, avoid sensitive personal details, and use reset behavior when personalization should be cleared.

Risk: Personalization proposals could make the skill less effective or drift away from its core boundaries.

Mitigation: Review proposed profile changes before applying them and reject changes that conflict with the core reflection rules.

## Reference(s):

- [Cogito Patterns](references/cogito-patterns.md)
- [Evolution Guide](references/evolution-guide.md)
- [User Profile](references/user-profile.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown conversation text and profile update proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local user-profile Markdown file only after user confirmation]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
