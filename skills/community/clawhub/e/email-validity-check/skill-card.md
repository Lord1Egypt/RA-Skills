## Description:

Checks email address format and validity status through the UpKuajing Open Platform API to help clean contact lists and reduce outreach bounce rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, sales teams, recruiters, marketers, and B2B operators use this skill to validate one or more email addresses before outreach, CRM cleanup, candidate screening, supplier verification, or list scrubbing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reads an UpKuajing API key and uses a paid API account.

Mitigation: Install only if the user trusts UpKuajing with submitted email addresses and the associated paid API account; review permissions on ~/.upkuajing/.env.

Risk: Email addresses and abnormal request or response details may be sent to external UpKuajing services.

Mitigation: Avoid submitting sensitive addresses or sensitive request and response bodies in error reports, and confirm reports before sending them.

Risk: The skill includes account top-up and payment-order flows.

Mitigation: Require explicit user confirmation before running any top-up or payment-order command.

Risk: The skill includes undisclosed update-check behavior noted by the security evidence.

Mitigation: Review the version-check behavior during installation and deployment, especially in environments that restrict outbound network calls.

## Reference(s):

- [Email Validity API](references/email-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [UpKuajing homepage](https://www.upkuajing.com)
- [Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/email-validity-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; paid API calls may return fee and balance information.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
