## Description: <br>
钉钉/飞书集成 - 企业通讯、机器人、自动化工作流（Slack 中国版） <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and enterprise automation teams use this skill for guidance on DingTalk and Feishu/Lark messaging, bot integrations, scheduling, approvals, alerts, and workflow notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs, app IDs, app secrets, or tokens could be exposed in prompts, chats, logs, or generated examples. <br>
Mitigation: Keep credentials out of chats and logs, use placeholders in shared examples, and store real values in approved secret-management systems. <br>
Risk: Messages or reports sent through DingTalk or Feishu may expose local or sensitive business information to enterprise chat channels. <br>
Mitigation: Confirm the target workspace and channel before sending, test in a low-risk channel first, and verify that the content is approved for that audience. <br>
Risk: Automated notifications can send excessive or unintended messages. <br>
Mitigation: Apply rate limits and review notification triggers before using the examples in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/dingtalk-feishu-cn) <br>
- [DingTalk robot webhook endpoint](https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN) <br>
- [Feishu bot webhook endpoint](https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_HOOK) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes webhook examples, SDK setup snippets, platform comparison notes, and usage cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
