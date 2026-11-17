## Description:

Dataphin skills suite entry point that routes agent work to Dataphin sub-skills for data planning, integration, development, operations monitoring, security, data assets, data service API development, knowledge graph, and unstructured data workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data platform operators use this skill to route Dataphin automation requests to specialized sub-skills for setup, governance, API, asset, operations, and workflow tasks. It helps agents produce commands, configuration guidance, validation steps, and code snippets for Alibaba Cloud Dataphin workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on cloud credentials for Dataphin operations.

Mitigation: Configure credentials outside chat where possible, prefer short-lived credentials, and scope permissions to the least privilege needed for the requested task.

Risk: The skill may install or update CLI plugins and interact with network endpoints.

Mitigation: Pin and verify CLI and plugin installers before use, and review network settings before installing the skill in a real Dataphin environment.

Risk: Some routed workflows can perform write, permission, publish, delete, SQL, or shell actions.

Mitigation: Require explicit human confirmation before executing state-changing, permission-changing, SQL, or shell commands.

Risk: TLS bypass or HTTP-style diagnostic settings can weaken transport protections.

Mitigation: Avoid TLS bypass except in controlled diagnostics and restore normal certificate verification for routine use.

## Reference(s):

- [CLI Installation Guide](references/cli-installation-guide.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [RAM Policies](references/ram-policies.md)
- [Version-Aware OpenAPI Reference](references/version-aware-openapi.md)
- [Related Commands](references/related-commands.md)
- [Aliyun CLI](https://github.com/aliyun/aliyun-cli)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-dataphin-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Dataphin CLI commands, OpenAPI request guidance, validation checks, and human-confirmation prompts before write or permission-changing actions.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
