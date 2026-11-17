## Description:

Manage Alibaba Cloud EMR Serverless Spark workspaces, Spark jobs, Kyuubi interactive queries, resource queue scaling, and status and log queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to operate Alibaba Cloud EMR Serverless Spark environments, including workspace setup, Spark job submission, Kyuubi SQL access, queue scaling, monitoring, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent operating Alibaba Cloud EMR Serverless Spark with cloud credentials.

Mitigation: Use least-privilege RAM roles, scope credentials to the required workspace and operations, and avoid FullAccess policies for routine workflows.

Risk: Installer and plugin-update steps can introduce supply-chain exposure.

Mitigation: Verify the Alibaba Cloud CLI installer independently, review plugin sources, and keep CLI auto-plugin installation disabled unless that risk has been explicitly accepted.

Risk: Public Kyuubi endpoints and Kyuubi tokens can expose interactive SQL access.

Mitigation: Prefer private endpoints, restrict allowed networks, rotate tokens, and avoid pasting real tokens into command examples or chat transcripts.

Risk: Some supported operations can interrupt or delete running jobs, sessions, tokens, or Kyuubi services.

Mitigation: Perform the documented status checks and require explicit user confirmation before cancellation, stop, or delete operations.

Risk: Workspace deletion is explicitly outside this skill's supported risk posture.

Mitigation: Reject workspace deletion through the agent path and direct users to the EMR Serverless Spark Console for that operation.

## Reference(s):

- [Getting Started](references/getting-started.md)
- [Workspace Lifecycle](references/workspace-lifecycle.md)
- [Job Management](references/job-management.md)
- [Kyuubi Service](references/kyuubi-service.md)
- [Scaling Guide](references/scaling.md)
- [RAM Permission Policies](references/ram-policies.md)
- [API Parameter Reference](references/api-reference.md)
- [Alibaba Cloud CLI Credential Management](https://help.aliyun.com/document_detail/110341.html)
- [EMR Serverless Spark Console](https://emr-next.console.aliyun.com/#/region/cn-hangzhou/resource/all/serverless/spark/list)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Alibaba Cloud CLI commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Alibaba Cloud credentials and aliyun CLI >= 3.3.3; includes mandatory user-agent usage and explicit confirmation guidance for destructive operations.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
