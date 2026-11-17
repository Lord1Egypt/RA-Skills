## Description:

Analyzes email headers to extract authentication, routing, and security metadata for threat detection and email forensics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, incident responders, email administrators, and forensic investigators use this skill to analyze raw email headers for sender origin, routing path, authentication results, and suspicious indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email headers sent for analysis may contain sensitive personal addresses, internal hostnames, message IDs, routing details, or incident data.

Mitigation: Confirm organizational approval before use, redact unnecessary sensitive header details where possible, and follow applicable data retention and incident handling policies.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/email-header-analyser)
- [Email Header Analyser API Route](https://api.mkkpro.com/security/email-header-analyser)
- [Email Header Analyser API Docs](https://api.mkkpro.com:8016/docs)

## Skill Output:

**Output Type(s):** [Analysis, API Calls]

**Output Format:** [JSON response with extracted email header metadata and suspicious indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits raw email header text to a third-party API service for analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
