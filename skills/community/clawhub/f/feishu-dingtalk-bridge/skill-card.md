## Description: <br>
Bridges Feishu and DingTalk APIs to support schedule synchronization, approval tracking, document parsing, and task distribution for enterprise workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operations teams, project managers, and enterprise workflow developers use this skill to turn Feishu or DingTalk calendar, approval, document, and task data into structured workflow reports and actionable task lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu or DingTalk enterprise access tokens and may process sensitive enterprise workflow data. <br>
Mitigation: Use least-privilege app tokens, provide secrets through a secure secret mechanism, avoid pasting real tokens into shared chats or repositories, and confirm tokens are masked in logs and outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boboy-j/feishu-dingtalk-bridge) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown report with tables, summaries, next actions, and automation suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires platform, action, auth_token, and optional query_context inputs; outputs should mask or omit access tokens and sensitive employee fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
