## Description:

Enriches a LinkedIn profile URL with profile details and a verified work email through Cargo and aiArk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development representatives and account executives use the skill to enrich known LinkedIn profile URLs with role, company, work history, and a verified work email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact URLs may contain information the user is not authorized to share with Cargo and aiArk.

Mitigation: Use only contact URLs the user is authorized to share with both providers.

Risk: A large batch can incur costs that scale with the number of successful enrichments.

Mitigation: Check the sample cost and results before approving a larger batch.

Risk: The CLI and any additional skill pack are external components outside this artifact review.

Mitigation: Review or pin the CLI and any additional skill pack before installation.

## Reference(s):

- [Cargo GTM Skills](https://github.com/getcargohq/gtm-skills)
- [Prospecting recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/prospecting.md)
- [ClawHub skill listing](https://clawhub.ai/cargo-ai/skills/enrich-linkedin-profile)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Structured person profile and work email data, with Markdown instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A result may be empty when no email is found; batch credit usage scales with the number of successful enrichments.]

## Skill Version(s):

1.1.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
