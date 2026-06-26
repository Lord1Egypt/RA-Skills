## Description: <br>
DataWorks data development skill for creating, configuring, validating, deploying, updating, moving, and renaming DataWorks nodes and workflows while managing components, resources, UDF functions, scheduling, and Data Integration pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to build and operate Alibaba Cloud DataWorks data development assets, including FlowSpec node definitions, workflows, scheduling configuration, deployment pipeline commands, and verification steps. It is intended for agents working with Aliyun CLI or Python SDK workflows that require validated specs, least-privilege credentials, and explicit confirmation for high-impact production actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact DataWorks production deployments, offline actions, pipeline cancellation, and mutating project operations. <br>
Mitigation: Require explicit human approval before Online or Offline deployments, cancellation, move, rename, or other mutating operations; verify deployment status from DataWorks responses before reporting success. <br>
Risk: The skill requires access to sensitive Alibaba Cloud credentials and DataWorks projects. <br>
Mitigation: Use least-privilege, non-root, preferably temporary credentials, avoid printing secrets, and restrict permissions to the target project and required DataWorks APIs. <br>
Risk: Generated SQL, shell nodes, DI jobs, preSql/postSql hooks, and DROP/DELETE/TRUNCATE statements may modify or destroy data. <br>
Mitigation: Review generated specs and code before execution, use non-production projects first, and keep backups or rollback plans for data-changing operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-dataworks-datastudio-develop) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [FlowSpec Format Reference](artifact/references/flowspec-guide.md) <br>
- [Workflow Development Guide](artifact/references/workflow-guide.md) <br>
- [Deployment Guide](artifact/references/deploy-guide.md) <br>
- [DataWorks Data Development API Call Templates](artifact/references/api-recipes.md) <br>
- [DI Data Synchronization Development Guide](artifact/references/di-guide.md) <br>
- [Scheduling Configuration Guide](artifact/references/scheduling-guide.md) <br>
- [DataWorks Data Development RAM Permission List](artifact/references/ram-policies.md) <br>
- [DataWorks Data Development Verification Methods](artifact/references/verification-method.md) <br>
- [Troubleshooting Guide](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with JSON, shell command, Python SDK, SQL, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DataWorks FlowSpec JSON, node directories, deployment commands, validation steps, and operational checklists.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
