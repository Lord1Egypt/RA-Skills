## Description: <br>
Alibaba Cloud SLS (Simple Log Service) log query and analysis skill that helps users write, explain, optimize, execute, and troubleshoot SLS index search, SQL analytics, and SPL scan/pipeline statements through the aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and cloud operators use this skill to translate log-analysis requests into Alibaba Cloud SLS index search, SQL, or SPL statements, execute or present aliyun CLI commands, and troubleshoot query results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Alibaba Cloud SLS queries through a local aliyun CLI profile, so an overprivileged profile could expose more log data than intended. <br>
Mitigation: Use least-privilege RAM permissions scoped to the required projects and logstores, and prefer temporary credentials or RAM roles where available. <br>
Risk: Credential material could be exposed if users paste access keys into chat or commands echo secrets. <br>
Mitigation: Do not paste access keys into chat; verify credential status only with `aliyun configure list` and redact any credential values from outputs. <br>
Risk: CLI installation or update commands may fetch remote installers or binaries. <br>
Mitigation: Review remote installer commands before running them and install the aliyun CLI only from intended Alibaba Cloud sources. <br>
Risk: Incorrect region, endpoint, timezone, or time range choices can produce misleading incident or compliance query results. <br>
Mitigation: Confirm region and timezone assumptions before executing sensitive queries, use documented endpoint discovery when needed, and generate `--from` and `--to` as Unix seconds. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-sls-query) <br>
- [Query & Analysis Routing](references/query-analysis.md) <br>
- [SPL Usage Guide](references/spl-guide.md) <br>
- [Function Selection Guide](references/functions-guide.md) <br>
- [Query & Analysis Troubleshooting](references/troubleshooting.md) <br>
- [Related APIs - SLS Query & Analysis](references/related-apis.md) <br>
- [RAM Policies - SLS Query Analysis](references/ram-policies.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Region & Endpoint Configuration](references/regions.md) <br>
- [Acceptance Criteria: sls-query-analysis](references/acceptance-criteria.md) <br>
- [Alibaba Cloud SLS GetLogsV2 API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-getlogsv2) <br>
- [Alibaba Cloud SLS GetIndex API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-getindex) <br>
- [Alibaba Cloud SLS GetProject API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-getproject) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, SQL, SPL, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces copy-paste-ready aliyun CLI commands, query statements, result summaries, and troubleshooting guidance; commands should redact credentials and include the required per-session user-agent for Alibaba Cloud API calls.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
