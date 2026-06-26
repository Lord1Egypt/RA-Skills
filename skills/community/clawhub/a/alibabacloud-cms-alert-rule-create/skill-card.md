## Description: <br>
Create and query Alibaba Cloud alert rules via CLI for CMS 1.0 cloud resource monitoring and CMS 2.0 Prometheus, APM, and UModel monitoring, with intent routing to select the appropriate workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to create, query, and verify Alibaba Cloud CMS alert rules from the Alibaba Cloud CLI while collecting required parameters and confirming changes before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Alibaba Cloud CLI operations with real credentials and may change alerting configuration. <br>
Mitigation: Use least-privilege RAM permissions, review generated commands, and require explicit confirmation before write operations. <br>
Risk: Disable, delete, or update actions can reduce or remove monitoring coverage. <br>
Mitigation: Treat those actions as administrative changes and verify the target rule, workspace, and region before execution. <br>
Risk: The skill enables aliyun AI mode during setup, which may leave a local CLI setting enabled after use. <br>
Mitigation: Run the documented cleanup step, `aliyun configure ai-mode disable`, when the workflow is complete. <br>
Risk: Incorrect routing between CMS 1.0 and CMS 2.0 workflows can produce invalid commands or misleading alert behavior. <br>
Mitigation: Follow the skill's intent routing and API enforcement rules, and stop rather than falling back to a different API when a required API fails. <br>


## Reference(s): <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Critical Rules](artifact/references/critical-rules.md) <br>
- [RAM Policies](artifact/references/ram-policies.md) <br>
- [CMS 1.0 Query Workflow](artifact/references/step-query.md) <br>
- [CMS 1.0 Preview and Execute Workflow](artifact/references/step5-preview-execute.md) <br>
- [CMS 2.0 Query Workflow](artifact/references/cms2-step-query.md) <br>
- [CMS 2.0 Preview and Execute Workflow](artifact/references/cms2-step5-preview-execute.md) <br>
- [Prometheus Metrics](artifact/references/prometheus-metrics.md) <br>
- [APM Metrics](artifact/references/apm-metrics.md) <br>
- [Alibaba Cloud CMS Console](https://cms.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before cloud write operations and uses Alibaba Cloud CLI commands.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
