## Description:

ADBPG Knowledge Base Management: Create knowledge bases, upload documents, search, and run Q&A over Alibaba Cloud AnalyticDB for PostgreSQL knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and cloud administrators use this skill to create and manage ADBPG knowledge bases, upload documents, search indexed content, and run knowledge-base Q&A. It guides users through Alibaba Cloud CLI and Python SDK workflows with parameter confirmation, RAM permission checks, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to change Alibaba Cloud CLI setup, including AI-mode, automatic plugin installation, plugin updates, and a custom User-Agent.

Mitigation: Install or update the CLI and plugins only through verified vendor or package-manager sources, confirm the configuration changes before use, and disable AI-mode after the workflow completes.

Risk: Knowledge-base operations require cloud credentials and database or namespace passwords.

Mitigation: Use least-privilege RAM credentials, configure credentials outside chat and command history, avoid pasting reusable passwords into conversations or literal command lines, and verify required permissions before write operations.

Risk: Document upload can send local or remote files to Alibaba Cloud services.

Mitigation: Confirm file paths, URLs, collection names, and endpoints before upload, and verify non-default endpoints before sending files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-analyticdb-postgresql-knowledgebase-ops)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [ADBPG API documentation](https://help.aliyun.com/zh/analyticdb-for-postgresql/developer-reference/api-reference)
- [ADBPG OpenAPI documentation](https://api.aliyun.com/product/gpdb)
- [CLI installation guide](references/cli-installation-guide.md)
- [RAM policies](references/ram-policies.md)
- [Related APIs](references/related-apis.md)
- [Interaction guidelines](references/interaction-guidelines.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Alibaba Cloud CLI commands, parameter confirmation prompts, SDK upload guidance, and verification steps.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
