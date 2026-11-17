## Description:

This skill helps agents use Laiye ADP to extract structured JSON fields from Chinese household register images, scans, URLs, Base64 payloads, and batch inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

External users, developers, and operations teams use this skill to route Chinese household register documents through Laiye ADP and receive structured fields for identity verification, information entry, account opening review, and related document workflows.

### Deployment Geography for Use:

Global, with separate China mainland and overseas ADP service endpoints.

## Known Risks and Mitigations:

Risk: Remote installer commands can execute unverified code during setup.

Mitigation: Prefer the npm package or a pinned release with verification; avoid curl-to-bash and PowerShell iex installer paths.

Risk: Household register inputs and outputs contain sensitive identity, address, and family relationship data.

Mitigation: Use the skill only for documents the user is authorized to upload to Laiye ADP, and review output storage before use in shared or regulated environments.

Risk: API credentials and document-processing outputs may persist in local configuration or export locations.

Mitigation: Check where ADP credentials, cached app IDs, task files, and exported JSON results are stored before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laiye-adp/skills/adp-household-register-recognition-and-extract)
- [Laiye ADP China mainland portal](https://adp.laiye.com/?utm_source=clawhub)
- [Laiye ADP overseas portal](https://adp-global.laiye.com/?utm_source=clawhub)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and structured JSON extraction results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local files, URLs, Base64 input, batch export files, and async task IDs; household register fields are returned as field_key, field_name, and field_values objects.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
