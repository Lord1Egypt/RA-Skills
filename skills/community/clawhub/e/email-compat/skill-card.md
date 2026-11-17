## Description:

Helps developers write and check HTML emails for rendering compatibility across email clients using caniemail support data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shbernal](https://clawhub.ai/user/shbernal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email designers use this skill to build HTML email templates and check their markup against email-client support data, including workarounds for unsupported features. It does not send email or assess deliverability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: By default, compatibility checks fetch public caniemail data and store a local cache.

Mitigation: Use --offline to skip network access, and review the reported data source and freshness before relying on a result.

Risk: Untested or older compatibility data may not predict how a particular email client renders a message.

Mitigation: Treat untested findings as unknown and test important templates in the target clients.

## Reference(s):

- [Caniemail compatibility data](https://www.caniemail.com/)
- [Email Compatibility on ClawHub](https://clawhub.ai/shbernal/skills/email-compat)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Prose or Markdown guidance, HTML/CSS suggestions, and JSON compatibility findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings identify affected clients and support verdicts; results indicate whether compatibility data is live, cached, or bundled.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
