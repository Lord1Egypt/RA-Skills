## Description: <br>
Helps agents execute Alibaba Cloud Flink, Ververica, and Realtime Compute Console workspace operations through the bundled Python CLI for drafts, SQL checks, deployments, jobs, session clusters, tables, members, variables, and checkpoint diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and platform operators use this skill to run scoped Alibaba Cloud Flink Console workspace tasks, including SQL draft validation, deployment and job operations, session cluster lifecycle actions, workspace administration, and diagnostics. It is intended for live workspace operations and expects the agent to execute the provided CLI rather than produce plans or mock output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live changes to Alibaba Cloud Flink workspace resources. <br>
Mitigation: Install and run it only in a sandbox or tightly scoped Alibaba Cloud account unless live workspace changes are intended. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials. <br>
Mitigation: Use least-privilege RAM policies, avoid production credentials, and do not persist long-lived access keys in shell profiles. <br>
Risk: Mutating and destructive commands may affect deployments, jobs, members, variables, and session clusters. <br>
Mitigation: Review every command that includes `--confirm` before execution and verify state with read-back commands after mutations. <br>
Risk: The generic Flink API proxy can broaden what the agent can reach. <br>
Mitigation: Avoid proxy-style commands unless the target backend endpoint and expected effect are fully understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-flink-workspace-ops) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Agent Operating Protocol](references/agent-operating-protocol.md) <br>
- [Command Catalog](references/command-catalog.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output summaries; some commands can emit JSON, table, or text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python dependencies and Alibaba Cloud credentials via the default credential chain; mutating and destructive operations require explicit confirmation flags.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
