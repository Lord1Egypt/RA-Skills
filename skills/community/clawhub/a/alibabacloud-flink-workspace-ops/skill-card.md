## Description:

Enables agents to operate Alibaba Cloud Flink and Ververica Console workspace resources through the bundled Python CLI, including SQL drafts, validation, deployments, jobs, session clusters, workspace administration, table lookup, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to route explicit Alibaba Cloud Flink workspace requests into concrete CLI operations for drafts, SQL validation, deployments, jobs, session clusters, members, variables, tables, and diagnostics. It is intended for scoped workspace operations, not instance lifecycle, generic cloud infrastructure, billing, storage, or unrelated workspace contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive live Alibaba Cloud Flink workspace changes, including when scope is missing or placeholder IDs are used.

Mitigation: Use least-privilege temporary credentials and verify workspace, namespace, region, deployment, job, session cluster, and other resource IDs before permitting mutation or deletion.

Risk: Commands such as UDF, connector, execute_sql, deployment-target, and API-proxy operations can materially affect workspace behavior.

Mitigation: Restrict RAM permissions to the smallest needed action set and require careful review before allowing these commands in production workspaces.

Risk: Long-lived cloud credentials may be exposed or reused if stored in shell startup files or logs.

Mitigation: Prefer temporary credentials, avoid persisting access keys in shell profiles, and do not print or store credential values in command output or generated artifacts.

## Reference(s):

- [Agent Operating Protocol](references/agent-operating-protocol.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Command Catalog](references/command-catalog.md)
- [Command Map Index](references/command-map.md)
- [Error Handling](references/error-handling.md)
- [RAM Policies for Flink Console Operations](references/ram-policies.md)
- [Related APIs](references/related-apis.md)
- [Resource Loading Policy](references/resource-disclosure.md)
- [Verification Methods](references/verification-method.md)
- [VVP Product Concept Model](references/vvp-product-model.md)
- [Playbook: Create -> Validate -> Deploy](references/playbooks/create-validate-deploy.md)
- [Playbook: List -> Filter -> Act](references/playbooks/list-filter-act.md)
- [Playbook: Session Cluster Lifecycle](references/playbooks/session-cluster-lifecycle.md)
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-flink-workspace-ops)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls, JSON]

**Output Format:** [Markdown with inline shell commands and JSON, table, or text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include direct cloud-operation results and follow-up guidance; mutating and destructive operations rely on explicit confirmation gates and read-back verification.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
