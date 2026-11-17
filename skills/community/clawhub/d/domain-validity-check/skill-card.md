## Description:

Verify corporate domain status to filter invalid domains, boost email deliverability, and clean CRM and email lists for exporters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, marketers, researchers, and CRM operators use this skill to check corporate domain validity, security, and sensitivity status before outreach, list cleansing, or lead verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Domain data is sent to UpKuajing's remote API.

Mitigation: Use the skill only with domains that are appropriate to share with UpKuajing.

Risk: The skill uses a paid API and stores UPKUAJING_API_KEY locally.

Mitigation: Confirm fees before API calls and restrict ~/.upkuajing and ~/.upkuajing/.env to owner-only permissions after setup.

Risk: Error reports may include customer or request context.

Mitigation: Avoid sharing raw customer data in error reports and submit reports only after explicit confirmation.

Risk: The skill performs a remote version check.

Mitigation: Review the outbound version-check behavior before installing or running in restricted environments.

## Reference(s):

- [Domain Validity API](references/domain-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/domain-validity-check)
- [UpKuajing Homepage](https://www.upkuajing.com)
- [UpKuajing Developer Portal](https://developer.upkuajing.com/)
- [UpKuajing OpenAPI Pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON results with domain status, sensitivity status, fee information, and request id; supporting guidance may be returned as Markdown or shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, httpx, and UPKUAJING_API_KEY; domain-check API calls may incur fees.]

## Skill Version(s):

1.0.2 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
