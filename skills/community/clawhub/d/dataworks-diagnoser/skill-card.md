## Description: <br>
Fetches and analyzes Alibaba Cloud DataWorks task instance logs to diagnose failures and recommend next steps using an instance ID and Alibaba Cloud credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljw-git-dw](https://clawhub.ai/user/ljw-git-dw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to fetch failed DataWorks task instance logs, analyze known error patterns such as ODPS, DataX, Java, resource, network, and permission failures, and generate actionable diagnosis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud credentials are required to fetch DataWorks logs. <br>
Mitigation: Use least-privilege RAM AccessKeys limited to documented read operations, prefer environment variables or protected Aliyun profiles over command-line secrets, and restrict permissions on credential files. <br>
Risk: Fetched logs and saved reports may contain SQL, endpoints, stack traces, or secrets. <br>
Mitigation: Treat logs and reports as sensitive, avoid sharing them broadly, and redact sensitive values before storing or forwarding diagnostic output. <br>
Risk: Automated diagnosis can miss context or provide incomplete remediation guidance. <br>
Mitigation: Review the generated diagnosis against the DataWorks console, task configuration, and relevant Alibaba Cloud documentation before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ljw-git-dw/dataworks-diagnoser) <br>
- [DataWorks error code reference](references/error_codes.md) <br>
- [Alibaba Cloud DataWorks documentation](https://help.aliyun.com/product/27728.html) <br>
- [DataWorks public API reference](https://api.aliyun.com/api/dataworks-public) <br>
- [GetTaskInstanceLog API reference](https://api.aliyun.com/api/dataworks-public/2024-05-18/GetTaskInstanceLog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain-text diagnostic reports, optional JSON output, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch logs through Alibaba Cloud APIs and may save raw logs or diagnosis reports when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
