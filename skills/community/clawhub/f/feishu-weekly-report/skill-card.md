## Description: <br>
生成飞书周报：通过飞书 API 拉取指定时间范围的聊天记录并读取本地 daily memory 日志，合并素材后按用户指定模板整理输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hakityc](https://clawhub.ai/user/hakityc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and individual contributors use this skill to compile weekly work reports or work summaries from Feishu chat messages and local daily memory notes. It organizes collected work items into a concise weekly-report structure or a user-provided template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Feishu app credentials from the local OpenClaw configuration and use them to fetch chat history. <br>
Mitigation: Install only when the skill is trusted with those credentials, use a least-privilege Feishu app, and confirm the intended chat IDs and date range before each fetch. <br>
Risk: Fetched Feishu messages and local daily memory files may contain sensitive work information. <br>
Mitigation: Review the selected workspace memory files and generated report before sharing, and restrict collection to the minimum relevant time range and chats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hakityc/feishu-weekly-report) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu messages API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown weekly report with optional JSON lines message collection from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally write daily memory notes under the workspace memory directory when the user agrees.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
