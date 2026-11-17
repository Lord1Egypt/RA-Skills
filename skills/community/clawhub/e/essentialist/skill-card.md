## Description:

Essentialist is an API-first outbound revenue skill for agents that deploys sales campaigns, sources prospects, handles email sequencing and replies, qualifies leads, and books meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keddleman](https://clawhub.ai/user/keddleman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and revenue operators use this skill to connect an agent to the Essentialist platform for outbound sales workflows, including registration, campaign setup, contact-list import, monitoring, and lead reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer an agent toward registration, contact uploads, campaign activation, or bulk email sends without clear user consent.

Mitigation: Require explicit user confirmation before registration, contact import, campaign activation, and bulk send operations.

Risk: The skill routes outbound-sales activity and contact data through an external service.

Mitigation: Install only when external Essentialist platform operation is intended, and pin ESSENTIALIST_API_URL to a verified Essentialist-owned HTTPS hostname.

Risk: Mailgun credentials and upgrade or payment flows may be handled during setup.

Mitigation: Require explicit confirmation before Mailgun credential submission and before presenting or using upgrade/payment links.

Risk: The documented registration flow can return existing credentials for an already registered email address.

Mitigation: Confirm that the existing-credentials registration behavior has been fixed before deployment.

## Reference(s):

- [Essentialist API Reference](references/api-reference.md)
- [Cold Email Best Practices](references/email-best-practices.md)
- [Essentialist Agent Entry Point](https://agents.essentialist.io)
- [Essentialist Website](https://essentialist.io)
- [ClawHub Skill Page](https://clawhub.ai/keddleman/skills/essentialist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, ESSENTIALIST_API_URL, and ESSENTIALIST_API_KEY for authenticated platform operations.]

## Skill Version(s):

5.1.0 (source: server release evidence; artifact frontmatter and clawhub.json show 4.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
