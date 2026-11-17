## Description:

Enterprise customer-management skill that helps agents query customer profiles, assemble customer portraits, surface risk alerts, and produce customer timelines from Excel ledger data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise service and property-management staff use this skill to retrieve tenant records, summarize customer activity, identify fee or renewal risks, and build customer timelines for operational follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A WeCom webhook credential appears in the skill content.

Mitigation: Remove the embedded credential, rotate the exposed key, and require deployers to provide approved webhook secrets through their own secret-management process.

Risk: Scheduled or group-chat reporting may expose sensitive customer, contract, fee, and risk data.

Mitigation: Require explicit recipient configuration, approved business purpose, data minimization, redaction of sensitive fields, and auditable delivery logs before enabling scheduled reports.

Risk: The packaged executable code is placeholder-like and may not fully represent the runtime behavior described by the skill.

Mitigation: Review the final implementation and test the Excel-reading, risk-scoring, and outbound-notification behavior before deployment.

## Reference(s):

- [Reference Documentation for Customer Management](references/api_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/perrykono-debug/skills/enterprise-customer-management)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional Python snippets, scheduled task configuration, and structured customer-risk summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include customer, contract, fee, repair, and risk data read from configured Excel workbooks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
