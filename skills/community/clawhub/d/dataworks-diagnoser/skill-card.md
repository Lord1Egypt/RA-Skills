## Description:

Fetches and analyzes Alibaba Cloud DataWorks task instance logs to diagnose failures and recommend next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljw-git-dw](https://clawhub.ai/user/ljw-git-dw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to fetch DataWorks task logs, identify common ODPS, DataX, Java, resource, network, permission, and data quality failures, and produce actionable diagnostic reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Alibaba Cloud credentials and supports passing secrets through command-line arguments or local credential files.

Mitigation: Use a dedicated least-privileged RAM role or short-lived credentials, prefer environment or managed credential stores over command-line secrets, and keep credential files outside project directories with restrictive permissions.

Risk: Saved task logs and diagnostic reports may contain sensitive operational data.

Mitigation: Redact sensitive task details before sharing reports and avoid storing raw logs longer than needed.

Risk: The server security verdict is suspicious because the skill asks for broader permissions than its code appears to need.

Mitigation: Review requested permissions before installation and grant only the DataWorks log access required for the intended workflow.

## Reference(s):

- [DataWorks error code reference](references/error_codes.md)
- [Alibaba Cloud DataWorks documentation](https://help.aliyun.com/product/27728.html)
- [Alibaba Cloud DataWorks API reference](https://api.aliyun.com/api/dataworks-public)
- [GetTaskInstanceLog API](https://api.aliyun.com/api/dataworks-public/2024-05-18/GetTaskInstanceLog)
- [ClawHub skill page](https://clawhub.ai/ljw-git-dw/skills/dataworks-diagnoser)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance]

**Output Format:** [Plain text or JSON diagnostic reports, with optional saved log and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Alibaba Cloud DataWorks APIs and can save raw task logs or diagnostic reports when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
