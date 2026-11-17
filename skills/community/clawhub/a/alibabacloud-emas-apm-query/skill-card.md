## Description:

Alibaba Cloud EMAS APM troubleshooting skill that uses the aliyun emas-appmonitor read-only APIs to aggregate mobile app issues, drill into representative samples, map stacks to user source code, and produce root cause analysis and fix suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile reliability engineers use this skill to investigate Alibaba Cloud EMAS APM crash, ANR, lag, custom exception, memory leak, and memory allocation issues across Android, iOS, HarmonyOS, Flutter, and Unity applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials may be exposed if access keys are pasted into chat, shell history, or generated reports.

Mitigation: Use OAuth, STS, or managed roles where possible; verify profiles without printing secrets; keep Alibaba Cloud credential files out of generated artifacts.

Risk: Unpinned Aliyun CLI plugin updates may change executable behavior between runs.

Mitigation: Review plugin versions before use in controlled environments and avoid unattended auto-updates when reproducibility matters.

Risk: APM diagnostic outputs may contain user, device, IP, log, stack, and crash details.

Mitigation: Store generated reports and JSON samples in a private directory, limit sharing, and delete local diagnostic folders when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-emas-apm-query)
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md)
- [RAM permissions and failure handling](references/ram-policies.md)
- [GetIssues - aggregated error list](references/get-issues.md)
- [GetIssue - aggregated error detail](references/get-issue.md)
- [GetErrors - sample list](references/get-errors.md)
- [GetError - sample detail](references/get-error.md)
- [Troubleshooting workflow: from sample to code fix](references/troubleshoot-workflow.md)
- [biz-module reference](references/biz-module-reference.md)
- [filter structure and usage](references/filter-reference.md)
- [Success verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [EMAS console](https://emas.console.aliyun.com/)
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/en/cli/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports with inline shell commands, JSON evidence paths, and optional source-code fix suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local diagnostic JSON folders and concise code diffs when app source is available.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
