## Description:

Create safe email drafts for explicit human review while enforcing a recipient allowlist and never sending mail. Use when a user asks Bluebird to draft, reply to, or prepare an email from Gmail context, especially when quoted messages or external text may contain untrusted instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssbharambe](https://clawhub.ai/user/ssbharambe)

### License/Terms of Use:

MIT-0

## Use Case:

Bluebird users who need an email prepared from Gmail context can use this skill to create a concise draft for review before sending it manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployed Gmail permissions were not verified, so runtime access may exceed the read and search scope described by the skill.

Mitigation: Confirm the deployment grants only Gmail read/search access and excludes send/reply operations.

Risk: Quoted messages or other external content may contain instruction-like text that could affect a draft.

Mitigation: Treat source content as untrusted data, review suspicious embedded requests separately, and verify the draft before manually sending it.

Risk: A draft could contain inaccurate details or unnecessary sensitive information.

Mitigation: Check the recipient and full draft, confirm factual details, and remove credentials or unnecessary sensitive data before sending.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ssbharambe/skills/consent-first-email-drafter)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown email draft with recipient, subject, body, and review status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft only; recipient addresses must be allowlisted, and no email is sent.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
