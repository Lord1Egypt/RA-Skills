## Description: <br>
Invoke Alibaba Cloud Apsara Data Agent for Analytics via CLI to perform natural language-driven data analysis on enterprise databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to discover Alibaba Cloud DMS data resources, start natural language database or file analysis sessions, monitor progress, and retrieve generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses enterprise databases and Data Agent sessions with Alibaba Cloud credentials. <br>
Mitigation: Use least-privilege RAM credentials and prefer the custom minimal policy documented in references/RAM-POLICIES.md over broad managed DMS policies. <br>
Risk: Session directories can contain prompts, progress logs, reports, generated files, and other sensitive analysis artifacts. <br>
Mitigation: Treat all files under sessions/ as sensitive, restrict local access, and review artifacts before sharing them. <br>
Risk: External notification behavior can send session progress or results to configured push destinations. <br>
Mitigation: Review notification and logging behavior before installation, avoid setting ASYNC_TASK_PUSH_URL unless the destination is approved, and disable HEARTBEAT-style notifications for sensitive sessions. <br>
Risk: Deep analysis and insight modes can generate execution plans, SQL, reports, and charts that may be incorrect or require user approval. <br>
Mitigation: Review generated plans, SQL, and reports before relying on them, and use attach-based confirmation only after checking the proposed analysis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-data-agent-skill) <br>
- [Alibaba Cloud Credential Chain Documentation](https://help.aliyun.com/document_detail/378659.html) <br>
- [Data Agent API Key Console](https://agent.dms.aliyun.com/cn-hangzhou/api-key) <br>
- [COMMANDS.md](references/COMMANDS.md) <br>
- [WORKFLOWS.md](references/WORKFLOWS.md) <br>
- [ANALYSIS_MODE.md](references/ANALYSIS_MODE.md) <br>
- [RAM-POLICIES.md](references/RAM-POLICIES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce session logs, status files, downloaded reports, charts, and local artifacts under sessions/<SESSION_ID>/.] <br>

## Skill Version(s): <br>
1.8.5 (source: release evidence, SKILL.md metadata, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
