## Description: <br>
Generates visual health inspection reports for Alibaba Cloud PolarDB MySQL instances across resource monitoring, space analysis, slow queries, sessions, and alert history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and cloud operations engineers use this skill to inspect Alibaba Cloud PolarDB MySQL instances and generate local reports for single-instance, multi-instance, or full-account reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the configured Alibaba Cloud profile to read PolarDB, DAS, and CloudMonitor operational data. <br>
Mitigation: Use a dedicated least-privilege RAM profile scoped to the required read APIs before running inspections. <br>
Risk: Generated reports can contain sensitive SQL, session, and operational metadata. <br>
Mitigation: Choose a controlled output directory, restrict access to generated reports, and handle report files as sensitive operational data. <br>
Risk: The skill may modify local aliyun CLI plugin or configuration state while preparing required plugins and AI-mode settings. <br>
Mitigation: Preinstall required CLI plugins where possible, review local CLI configuration after use, and verify AI-mode and auto-plugin settings are in the expected state. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-polardb-mysql-inspection) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Manual Workflow](references/manual-workflow.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [Report Format](references/report-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, markdown, configuration, guidance] <br>
**Output Format:** [HTML reports by default, with text or Markdown report options and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files to a user-selected or default local output directory.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
