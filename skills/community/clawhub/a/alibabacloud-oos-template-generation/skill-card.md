## Description: <br>
OOS template intelligent generation skill for creating, writing, validating, and iteratively fixing Alibaba Cloud Operation Orchestration Service automation templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to draft Alibaba Cloud OOS automation templates from operational requirements, query OOS action metadata, and validate templates before presenting the final YAML or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an authenticated Aliyun CLI and may guide cloud mutation or execution workflows beyond template drafting. <br>
Mitigation: Review generated commands and templates before running them, grant least-privilege OOS permissions, and require explicit target confirmation before creating, deleting, or starting executions. <br>
Risk: Credential exposure could occur if access keys are pasted into shells, logs, or chat. <br>
Mitigation: Configure credentials outside the agent session, check only credential status, and avoid printing or requesting long-lived access keys. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-oos-template-generation) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [OOS Template Generation CLI Commands Reference](references/related-commands.md) <br>
- [RAM Policies for OOS Template Generation Skill](references/ram-policies.md) <br>
- [OOS Template Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud OOS Documentation](https://help.aliyun.com/zh/oos) <br>
- [OOS Template Syntax](https://help.aliyun.com/zh/oos/user-guide/template-syntax) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML or JSON code blocks and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated templates are expected to pass OOS validation before final output.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
