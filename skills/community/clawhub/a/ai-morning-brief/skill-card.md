## Description:

Morning Brief collects AI news from RSS feeds, configured blogwatcher sources, ClawdChat tool gateways, and OpenRouter ranking snapshots, then uses an LLM to select up to 10 high-value items for a Telegram daily brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[min870809](https://clawhub.ai/user/min870809)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation operators use this skill to generate a scheduled, personalized AI industry morning brief, reducing low-signal news while highlighting competitor updates and monetization opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically sends LLM-selected content to Telegram, which may be inappropriate for shared or public destinations.

Mitigation: Use a private Telegram destination or require human review before scheduled delivery.

Risk: API and Telegram credentials are needed to run the workflow.

Mitigation: Store tokens in environment variables or a secret manager, and avoid hardcoding secrets in the script.

Risk: The skill depends on API Hub and ClawdChat services as third-party data and tool providers.

Mitigation: Confirm those services are acceptable for the deployment before enabling the skill.

Risk: The workflow broadly marks blogwatcher items read after sending a brief.

Mitigation: Remove or narrow `blogwatcher read-all`, or add review before items are marked read.

Risk: Links and Telegram Markdown formatting may affect how generated brief content is displayed.

Mitigation: Validate links and escape Telegram formatting before scheduled delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/min870809/skills/ai-morning-brief)
- [Publisher profile](https://clawhub.ai/user/min870809)
- [Hugging Face Blog RSS](https://huggingface.co/blog/feed.xml)
- [人人都是产品经理 RSS](https://www.woshipm.com/feed)
- [OpenRouter Global Top Apps](https://openrouter.ai/apps)
- [ClawdChat tool gateway](https://clawdchat.cn/api/v1/tools/call)
- [API Hub default endpoint](https://api.mulerun.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-formatted AI news brief sent to Telegram, with setup and scheduling guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects up to 10 items and truncates Telegram messages near 4,000 characters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
