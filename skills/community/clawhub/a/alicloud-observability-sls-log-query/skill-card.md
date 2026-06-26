## Description: <br>
Query and troubleshoot logs in Alibaba Cloud Log Service (SLS) using query|analysis syntax and the Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to run time-bounded Alibaba Cloud SLS log searches, investigate errors, and summarize troubleshooting evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials to query SLS logs and may expose log contents. <br>
Mitigation: Use read-only, least-privilege credentials scoped to the required SLS projects and logstores, and avoid sharing printed log output unnecessarily. <br>
Risk: Credentials or sensitive log data could be accidentally echoed, saved, or committed. <br>
Mitigation: Keep credentials in environment variables, do not commit secrets, and review saved artifacts before sharing. <br>


## Reference(s): <br>
- [Query syntax](references/query-syntax.md) <br>
- [Python SDK](references/python-sdk.md) <br>
- [Troubleshooting templates](references/templates.md) <br>
- [Source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; helper scripts print JSON log rows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries require Alibaba Cloud SLS endpoint, project, logstore, time range, limit, and read-capable credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
