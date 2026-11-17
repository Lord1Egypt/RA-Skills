## Description:

Retrieves last year, last month, and same-month-last-year date references from UpKuaJing for customs trade data queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External trade analysts, export teams, and import-export professionals use this skill to get fiscal date reference values before constructing customs overview, trend, and trade intelligence queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses UPKUAJING_API_KEY and can read or write a local ~/.upkuajing/.env file.

Mitigation: Prefer an environment variable or secret manager; if the local file is used, keep ~/.upkuajing owner-only and set the .env file mode to 0600.

Risk: Normal date reference API calls are billable, and account top-up/payment-order creation can be initiated through the helper scripts.

Mitigation: Require explicit user confirmation before billable queries, top-up/payment-order creation, or pricing/account operations.

Risk: Error reports may send request context and related API troubleshooting data to UpKuaJing.

Mitigation: Report only abnormal failures after user approval, and review the context before sending.

Risk: API calls trigger a version check and local cache write outside the primary query response.

Mitigation: Review this background network request and local persistence behavior before installation or restricted-environment use.

## Reference(s):

- [Date Reference API](references/customs-overview-date-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/customs-overview-date)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [UpKuaJing API pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UPKUAJING_API_KEY and may include fee and requestId fields in API responses.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
