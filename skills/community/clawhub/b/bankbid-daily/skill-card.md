## Description:

Filters public financial-procurement notices by keyword into bank tender, purchase, award, supplier-solicitation, prequalification, and amendment alerts, then returns a daily Markdown digest and open-project list with near-deadline items highlighted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External business users such as financial IT vendors, banking equipment providers, security contractors, facilities contractors, and financial outsourcing providers use this skill to monitor current bank procurement opportunities and award notices that match their keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends keywords, optional license data, and a persistent device fingerprint containing host and account details to the vendor endpoint.

Mitigation: Review telemetry expectations before installation, avoid using sensitive keywords, and prefer an app-scoped identifier or a version with clearer telemetry documentation.

Risk: Subscription credentials may be exposed if embedded directly in cron command lines, logs, shell history, or shared automation files.

Mitigation: Store the SkillPay license in a protected environment or secret store and limit access to automation logs and scheduled task definitions.

Risk: The service output aggregates public procurement information and may omit expired, historical, or unsupported notices.

Mitigation: Use the digest as a monitoring aid and verify important opportunities against the original public procurement sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bankbid-daily)
- [Bank Bid Daily account and quota page](https://www.tokendidi.cn/bankbid/account)
- [Bank Bid Daily service endpoint](https://www.tokendidi.cn/api/bankbid/api/v1/bankbid-daily)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown digest by default, with optional JSON output and a report URL when returned by the service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user keywords; optional parameters include notice kind, institution family, days, JSON mode, and a SkillPay license.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact frontmatter lists 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
