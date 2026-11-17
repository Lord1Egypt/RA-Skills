## Description:

Bootstrap and manage an open, file-based CRM using the CRM-in-a-Box protocol for contacts, pipeline records, and interactions stored as NDJSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hybrid1labs](https://clawhub.ai/user/hybrid1labs)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and agents use this skill to set up and maintain a local CRM without SaaS dependency. It supports adding contacts, updating pipeline stages, logging interactions, searching records, and adapting stages or labels for vertical workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM records may contain sensitive customer, pipeline, and interaction data stored as plaintext files.

Mitigation: Use the skill only in a private, access-controlled directory or repository and restrict file permissions.

Risk: The artifact advertises hash-chain or tamper-evident behavior that the security evidence says should not be relied on.

Mitigation: Do not treat the CRM log as tamper-evident unless the implementation is fixed and independently reviewed.

Risk: Agent-made CRM changes can affect business records and decisions.

Mitigation: Review contact, pipeline, and interaction changes before using the data for business decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hybrid1labs/skills/crm-in-a-box-hybrid)
- [CRM-in-a-Box Repository](https://github.com/taylorhou/crm-in-a-box)
- [biz-in-a-box Protocol Family](https://biz-in-a-box.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local NDJSON CRM records and config.yaml.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
