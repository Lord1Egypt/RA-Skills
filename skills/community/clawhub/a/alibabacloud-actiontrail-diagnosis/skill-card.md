## Description:

Query and diagnose Alibaba Cloud ActionTrail audit events across one or more regions, with results as a 12-column event table or machine-readable JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and support engineers use the skill to investigate who performed Alibaba Cloud operations, when they happened, and which resources or source IPs were involved. It helps trace changes, sign-ins, API calls, and suspicious or failed activity from ActionTrail records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling can expose cloud secrets.

Mitigation: Use an explicit CLI profile with verified region IDs; avoid environment credentials with the CLI backend.

Risk: Broad or long-running audit queries can retrieve more sensitive event data than needed.

Mitigation: Use short-lived credentials limited to the two documented read-only APIs, verify region IDs, and keep time windows and filters narrow. Treat returned audit results as sensitive.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-actiontrail-diagnosis)
- [ActionTrail API reference](artifact/references/api-reference.md)
- [Lookup attribute guide](artifact/references/lookup-attribute.md)
- [Minimum read-only RAM policies](artifact/references/ram-policies.md)
- [Alibaba Cloud service mapping](artifact/references/service-mapping.md)
- [Network events catalog](artifact/references/network-events-catalog.md)
- [Alibaba Cloud CLI setup](https://help.aliyun.com/document_detail/121541.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [A 12-column Markdown event table with a plain-language summary, or machine-readable JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only returned audit events; JSON includes query scope and partial or truncation status. Sensitive event fields are masked by default.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
