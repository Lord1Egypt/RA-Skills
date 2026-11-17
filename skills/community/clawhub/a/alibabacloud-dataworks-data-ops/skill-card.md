## Description:

DataWorks Operations Center assistant for task and workflow operations, alert rule creation and management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

DataWorks operators, developers, and support engineers use this skill to inspect scheduled task and workflow state, retrieve instance logs, review dependencies, and check alert rules through Aliyun CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may lead users to run curl-to-bash or unverified latest binary installers.

Mitigation: Use a preinstalled or independently verified Aliyun CLI and confirm the installed version before using the skill.

Risk: Automatic plugin installation and CLI AI-mode change persistent local CLI behavior.

Mitigation: Review and intentionally enable these settings only when needed, then disable AI-mode after the workflow and document any persistent CLI configuration changes.

Risk: Broad DataWorks permissions can expose more workspace data than required.

Mitigation: Grant only the listed RAM actions for the specific DataWorks workspace instead of account-wide access.

Risk: Credential handling can expose Alibaba Cloud access keys if credentials are entered or printed in the agent session.

Mitigation: Configure credentials outside the agent session and use only credential status checks during skill execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-dataworks-data-ops)
- [Skill Source](artifact/SKILL.md)
- [RAM Permission List](artifact/references/ram-policies.md)
- [CLI Command Quick Reference](artifact/references/related-commands.md)
- [Success Verification Methods](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Aliyun CLI Installation and Configuration Guide](artifact/references/cli-installation-guide.md)
- [Official Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/)
- [Alibaba Cloud RAM Console](https://ram.console.aliyun.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require user-confirmed region, project, date, and resource identifiers before execution.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
