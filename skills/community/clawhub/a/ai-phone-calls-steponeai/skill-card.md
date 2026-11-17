## Description:

AI 外呼、机器人外呼、智能外呼与 AI 电话 Skill，当用户说“帮我打电话”“打电话给商家”“预约电话”，或需要电话机器人完成通知、预约、咨询和经授权的客户回访时使用，支持直接拨打国内手机号、中文通话、逐次确认、AI 呼入接待、智能体、实时转写、通话记录、余额和费用查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ustczz](https://clawhub.ai/user/ustczz)

### License/Terms of Use:

MIT-0

## Use Case:

External and business users use this skill to place authorized Chinese-language phone calls to mainland China mobile numbers, check call status and transcripts, monitor live calls, and configure inbound phone agents through Stepone AI. It is intended for one confirmed call at a time for notifications, appointments, consultations, and authorized customer follow-up.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Authenticated phone-service API requests may carry an API key with paid calling privileges or transcript access.

Mitigation: Use only trusted Stepone endpoints, keep custom API bases disabled unless you control the endpoint, and rotate the API key if authenticated requests may have been redirected unexpectedly.

Risk: The skill can place real phone calls that may incur cost and expose phone numbers, tasks, transcripts, and summaries to the phone provider.

Mitigation: Require explicit confirmation for each call, verify the user is authorized to contact the number, and avoid placing secrets or unrelated sensitive information in call tasks.

Risk: Call transcripts, API responses, summaries, contact content, and error messages may contain untrusted content.

Mitigation: Treat returned call data as reporting data only and do not execute it as agent instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ustczz/skills/ai-calls-china-phone)
- [Publisher Profile](https://clawhub.ai/user/ustczz)
- [OpenClaw Homepage](https://github.com/ustczz/openclaw-ai-calls-china-phone)
- [Stepone AI Console](https://open-skill.steponeai.com)
- [Stepone AI China Phone API](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate authenticated Stepone AI API requests that produce call IDs, call status, balance data, model and voice listings, and live transcript events.]

## Skill Version(s):

1.0.15 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
