## Description: <br>
This skill guides agents through Alibaba Cloud DataWorks Operations Center task, workflow, task instance, and alert rule operations using the Aliyun CLI and dataworks-public OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data platform operators, developers, and support engineers use this skill to inspect DataWorks task and workflow state, retrieve task instance logs, review dependencies and operation logs, and read alert rule details during troubleshooting and failure recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance includes a curl-to-bash installation path for the Aliyun CLI. <br>
Mitigation: Prefer a trusted package manager or manually verified installer; only use the setup script after independently trusting and verifying the source. <br>
Risk: The skill operates with sensitive Alibaba Cloud credentials and DataWorks RAM permissions. <br>
Mitigation: Use temporary or least-privilege RAM credentials scoped to required DataWorks actions, and do not pass or print access keys in commands or conversation. <br>
Risk: Reference material includes examples for services outside the DataWorks operations scope. <br>
Mitigation: Follow only the DataWorks task, workflow, task instance, and alert rule commands unless the user explicitly requests other Alibaba Cloud services. <br>


## Reference(s): <br>
- [RAM Permission List](references/ram-policies.md) <br>
- [CLI Command Quick Reference](references/related-commands.md) <br>
- [Success Verification Methods](references/verification-method.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires confirmed region, project, business date, resource identifiers, RAM permissions, and an existing Aliyun CLI credential profile.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
