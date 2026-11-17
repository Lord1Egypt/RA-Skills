## Description:

Bootstrap and manage an open, file-based CRM using the CRM-in-a-Box protocol for contacts, pipeline records, and interactions as NDJSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taylorhou](https://clawhub.ai/user/taylorhou)

### License/Terms of Use:

BSL 1.1

## Use Case:

Developers, operators, and sales teams use this skill to bootstrap a local CRM, log contacts and leads, track pipeline stages, and record customer interactions without relying on a SaaS CRM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM records can contain sensitive customer, contact, sales, and interaction data in plaintext append-only files.

Mitigation: Keep CRM directories private, use restrictive filesystem permissions and encrypted storage or backups, and define correction, redaction, and deletion handling before use.

## Reference(s):

- [biz-in-a-box protocol family](https://biz-in-a-box.org)
- [CRM-in-a-Box project link from artifact](https://github.com/taylorhou/crm-in-a-box)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to create or append local NDJSON CRM records and customize config.yaml.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
