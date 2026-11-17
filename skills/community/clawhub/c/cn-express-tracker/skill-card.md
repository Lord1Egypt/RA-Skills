## Description:

Queries package tracking information for Chinese and international carriers via the Kuaidi100 API, with local carrier auto-detection from tracking numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charles-lpf](https://clawhub.ai/user/charles-lpf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check package delivery status and present a formatted logistics timeline. It is useful when a user provides a tracking number or asks for courier, express, or logistics status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers and the Kuaidi100 customer identifier are sent to Kuaidi100 during package lookups.

Mitigation: Use the skill only when that disclosure is acceptable for the package being tracked.

Risk: API credentials can be exposed if stored in shell startup files or shared command history.

Mitigation: Prefer temporary environment variables or a protected secrets manager for EXPRESS_TRACKER_KEY and EXPRESS_TRACKER_CUSTOMER.

Risk: Untrusted or unusual tracking strings may behave unexpectedly until input validation is improved.

Mitigation: Avoid submitting untrusted tracking strings and ask for the carrier code when auto-detection is uncertain.

## Reference(s):

- [Kuaidi100 Open Platform Registration](https://api.kuaidi100.com/register/enterprise)
- [Kuaidi100 Dashboard](https://api.kuaidi100.com/home)
- [Kuaidi100 Carrier Codes](https://api.kuaidi100.com/manager/openapi/download/kdbm.do)
- [Cn Express Tracker on ClawHub](https://clawhub.ai/charles-lpf/skills/cn-express-tracker)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text tracking timeline with command-line setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Kuaidi100 API credentials and local command-line dependencies: curl, jq, and one MD5 utility.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
