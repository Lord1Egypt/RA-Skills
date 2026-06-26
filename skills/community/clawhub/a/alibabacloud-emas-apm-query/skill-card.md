## Description: <br>
Alibaba Cloud EMAS APM issue troubleshooting skill for querying read-only AppMonitor APIs, ranking mobile app issues, drilling into representative samples, mapping stacks to source code, and producing root-cause analysis with fix suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and mobile reliability engineers use this skill to investigate Alibaba Cloud EMAS APM crash, ANR, lag, custom exception, memory leak, and memory allocation issues across Android, iOS, HarmonyOS, Flutter, and Unity applications. It guides read-only Aliyun CLI queries, compares representative samples, and can map stack traces to application source for actionable remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive crash, device, user, and business-log data in local reports and raw JSON outputs. <br>
Mitigation: Use narrow time ranges and sample sizes, redact identifiers before sharing outputs, and delete generated emas-apm-dig-* directories after troubleshooting. <br>
Risk: The skill relies on an Aliyun CLI profile to read EMAS APM data. <br>
Mitigation: Use a dedicated read-only RAM profile limited to emasha:ViewIssues, emasha:ViewIssue, emasha:ViewErrors, and emasha:ViewError. <br>
Risk: Debug logging can include request and response details that may be sensitive. <br>
Mitigation: Avoid DEBUG logs unless required for diagnosis and review logs before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-emas-apm-query) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [AppKey and OS Detection](references/appkey-detection.md) <br>
- [RAM Permissions and Failure Handling](references/ram-policies.md) <br>
- [GetIssues API Reference](references/get-issues.md) <br>
- [GetIssue API Reference](references/get-issue.md) <br>
- [GetErrors API Reference](references/get-errors.md) <br>
- [GetError API Reference](references/get-error.md) <br>
- [Filter Reference](references/filter-reference.md) <br>
- [Biz Module Reference](references/biz-module-reference.md) <br>
- [Troubleshooting Workflow](references/troubleshoot-workflow.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Aliyun CLI Official Documentation](https://help.aliyun.com/en/cli/) <br>
- [Aliyun EMAS AppMonitor Read-Only Policy](https://help.aliyun.com/zh/ram/developer-reference/aliyunemasappmonitorreadonlyaccess) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline bash commands, JSON diagnostic artifacts, and optional minimal code diffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local emas-apm-dig-* folders containing raw JSON API responses and report.md during troubleshooting] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
