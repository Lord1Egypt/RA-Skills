## Description: <br>
自动分析飞书群消息，提取学习点和进化建议，并按计划生成报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolvzhao-lab](https://clawhub.ai/user/coolvzhao-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Feishu workspace or group operators use this skill to monitor selected group chats, extract recurring learning themes, and generate periodic learning reports and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact embeds reusable Feishu app credentials and fixed chat targets. <br>
Mitigation: Replace and rotate the embedded credentials before installation, and confirm the intended chat IDs before running the skill. <br>
Risk: The skill accesses Feishu group messages and stores analysis outputs locally. <br>
Mitigation: Use only with appropriate workspace and group consent, and decide whether local memory, logs, and temporary raw message files are acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolvzhao-lab/feishu-group-learning) <br>
- [Feishu tenant access token API endpoint used by artifact](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu messages API endpoint used by artifact](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Console text reports and Markdown memory entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily memory entries and append-only logs under the OpenClaw workspace memory path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
