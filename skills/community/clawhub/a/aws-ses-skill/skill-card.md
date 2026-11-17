## Description:

Guides developers through Amazon SES account checks, domain authentication, SMTP credential setup, test sending, and bounce monitoring, with written guidance for production access and Sendy integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airo7](https://clawhub.ai/user/airo7)

### License/Terms of Use:

MIT

## Use Case:

Developers and email administrators use this skill to configure and troubleshoot Amazon SES sending, verify domains and DNS, check account health, and plan production access and newsletter delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS credentials allow email sending and SES identity changes.

Mitigation: Use least-privilege IAM credentials, preview changes with dry-run flags, and confirm before sending mail or changing AWS resources.

Risk: SMTP passwords and API keys could be exposed in conversation or logs.

Mitigation: Keep secrets out of chat and logs; store generated credentials securely.

Risk: Sendy requests can affect external campaigns or subscriber data.

Mitigation: Require explicit confirmation before calling any Sendy endpoint.

## Reference(s):

- [AWS SES skill on ClawHub](https://clawhub.ai/airo7/skills/aws-ses-skill)
- [AWS SES production access](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html)
- [AWS SES SMTP credentials](https://docs.aws.amazon.com/ses/latest/dg/smtp-credentials.html)
- [AWS SES DKIM setup](https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim.html)
- [Sendy with Amazon SES](https://sendy.co/amazon-ses)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account and DNS checks may return structured status; sending and identity creation require explicit user confirmation.]

## Skill Version(s):

0.1.3 (source: server-resolved ClawHub release; skill frontmatter says 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
