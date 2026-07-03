## Description: <br>
Diagnoses historical lock wait issues on Alibaba Cloud PolarDB/RDS MySQL and identifies the complete lock chain and lock holder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to troubleshoot historical lock waits, deadlocks, and transaction blocking in Alibaba Cloud PolarDB/RDS MySQL using Aliyun CLI and DAS audit data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify the local Alibaba Cloud CLI setup and install or update CLI plugins. <br>
Mitigation: Review CLI installation and plugin update steps before execution, and run them only in an approved local environment. <br>
Risk: The skill uses Alibaba Cloud account and database diagnostic data that can include sensitive SQL, sessions, or audit output. <br>
Mitigation: Use a least-privilege RAM role, avoid exposing access keys, and treat all SQL and session output as sensitive. <br>
Risk: The required permissions include hdm:CreateLatestDeadLockAnalysis, which is classified as a write action. <br>
Mitigation: Grant only the documented DAS permissions for the target account and review the deadlock-analysis action before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-history-lock-diagnose) <br>
- [RAM permission policy list](references/ram-policies.md) <br>
- [Related CLI commands](references/related-commands.md) <br>
- [Diagnosis best practices](references/best-practices.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [Transaction lifecycle rules](references/transaction-lifecycle.md) <br>
- [Verification methods](references/verification-method.md) <br>
- [Alibaba Cloud DAS SQL Insight documentation](https://help.aliyun.com/zh/das/user-guide/sql-insight) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnosis summary with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes key findings instead of pasting full raw script output; timestamps should include milliseconds.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
