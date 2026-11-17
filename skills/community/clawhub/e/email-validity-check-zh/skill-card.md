## Description:

Validates email addresses through Upkuajing's API and returns availability status, reasons, totals, fees, and request identifiers for email list cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, recruiting, marketing, and operations teams use this skill to validate email addresses before outreach, CRM cleanup, candidate screening, supplier checks, and email list hygiene. It helps identify valid, invalid, unknown, or unchecked addresses and reduce avoidable email bounces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted email addresses are shared with Upkuajing's remote service for validation.

Mitigation: Confirm the user is authorized to submit the address list before validation and avoid sending sensitive or regulated contact data unless approved.

Risk: The skill uses paid API operations and includes recharge/order flows.

Mitigation: Disclose that validation may incur charges and wait for explicit user confirmation before paid validation, recharge, or order creation.

Risk: The API key may be read from or stored in ~/.upkuajing/.env.

Mitigation: Use a safer secret mechanism where possible and do not print, paste, or expose the contents of the credential file.

Risk: Error-reporting commands may send request context and response details to the platform.

Mitigation: Run error reporting only after user confirmation and avoid including unnecessary sensitive request or response data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/email-validity-check-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Email validity API reference](references/email-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful validation results include total count, per-email status and reason, fee information, and requestId.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
