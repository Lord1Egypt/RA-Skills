## Description:

Find verified work email addresses from a person's name and company domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales development and revenue operations teams use this skill to find and verify business email addresses for prospect records using a person's name and company domain, or a LinkedIn profile URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unrelated repository promotion and external skill-install actions, as well as an unpinned external install command.

Mitigation: Review and remove or clearly explain those actions, and pin and review the external command and its source before installation.

Risk: The handling of contact data is not made clear before email lookups, and the scanner review is incomplete because some references could not be resolved.

Mitigation: Clarify contact-data handling before a lookup and resolve the unavailable references as part of a complete security review.

## Reference(s):

- [Cargo GTM Skills homepage](https://github.com/getcargohq/gtm-skills)
- [Prospecting recipe](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/prospecting.md)
- [ClawHub skill page](https://clawhub.ai/cargo-ai/skills/find-work-email)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Text containing verified work email addresses and unresolved rows, with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unresolved or unusable records remain empty rather than receiving guessed addresses.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
