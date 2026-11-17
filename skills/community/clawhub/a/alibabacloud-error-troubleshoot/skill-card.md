## Description: <br>
Alibaba Cloud OpenAPI troubleshooting skill that helps diagnose API call failures using request IDs, error codes, or error messages through Aliyun CLI openapiexplorer plugin commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to troubleshoot Alibaba Cloud OpenAPI failures by looking up request logs, interpreting error details, checking RAM permission issues, and retrieving official error-code solutions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Request logs may contain account identifiers, caller IPs, request parameters, response bodies, or credential-adjacent fields. <br>
Mitigation: Redact sensitive log fields before presenting results, never print access keys or secrets, and avoid sharing raw logs broadly. <br>
Risk: Troubleshooting commands can query Alibaba Cloud request-log data using the configured Aliyun CLI profile. <br>
Mitigation: Confirm the user intends to troubleshoot with the active profile, check credentials only with safe status commands, and use the documented RAM policies for least-privilege access. <br>
Risk: A missing or expired request log can lead to misleading diagnosis if treated as the original API failure. <br>
Mitigation: Stop on NotFound.RequestLog, explain the possible scope or retention issue, and ask for a fresh request ID or the original application error code instead of looking up NotFound.RequestLog as an error-code solution. <br>


## Reference(s): <br>
- [OpenAPI Diagnostic Portal](https://api.aliyun.com/troubleshoot) <br>
- [OpenAPI Troubleshoot CLI API Reference](references/api-reference.md) <br>
- [Aliyun CLI Installation & Plugin Setup](references/cli-installation-guide.md) <br>
- [RAM Policies for OpenAPI Troubleshoot](references/ram-policies.md) <br>
- [OpenAPI Troubleshoot Diagnostic Workflow](references/troubleshooting-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash commands and diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include redacted Alibaba Cloud request-log fields, official solution summaries, RAM policy snippets, and copy-paste-ready Aliyun CLI commands.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
