## Description: <br>
Manage the full lifecycle of Alibaba Cloud EMR Serverless Spark workspaces, including workspace creation, Spark job submission, Kyuubi interactive queries, resource queue scaling, and status queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to manage Alibaba Cloud EMR Serverless Spark resources, run Spark jobs, inspect logs and status, operate Kyuubi services, and adjust resource queues through guided CLI/API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide access-control, role-grant, public endpoint, token, queue scaling, and paid resource creation operations. <br>
Mitigation: Use a dedicated least-privilege RAM user or role, avoid FullAccess for normal job/query work, and manually approve member additions, role grants, public endpoints, token changes, queue scaling, and paid resource creation. <br>
Risk: Kyuubi tokens can be exposed through prompts, logs, shell history, or command-line arguments. <br>
Mitigation: Do not place real Kyuubi tokens in prompts, logs, shell history, or command-line arguments; use secret-handling practices outside the agent conversation. <br>
Risk: Workspace deletion is irreversible and is intentionally outside this skill's supported operations. <br>
Mitigation: Reject DeleteWorkspace requests in the agent workflow and direct users to the EMR Serverless Spark console for any workspace deletion decision. <br>


## Reference(s): <br>
- [Getting Started: Create Your First Spark Workspace from Scratch and Submit a Job](references/getting-started.md) <br>
- [Workspace Lifecycle: Create, Query, Manage](references/workspace-lifecycle.md) <br>
- [Job Management: Submit, Monitor, Diagnose Spark Jobs](references/job-management.md) <br>
- [Kyuubi Service: Interactive SQL Gateway Management](references/kyuubi-service.md) <br>
- [Scaling: Resource Queue Management](references/scaling.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [API Parameter Reference](references/api-reference.md) <br>
- [Alibaba Cloud CLI Credential Management](https://help.aliyun.com/document_detail/110341.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands, CLI examples, API parameters, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Alibaba Cloud CLI aliyun >= 3.3.3 or Python SDK, Alibaba Cloud credentials, required EMR Serverless Spark RAM roles, explicit User-Agent, and manual confirmation for destructive or sensitive operations.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
