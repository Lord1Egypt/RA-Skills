## Description:

Generates AI industry daily reports as Feishu-ready message content from recent, source-linked AI news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c1028874817-beep](https://clawhub.ai/user/c1028874817-beep)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and operators use this skill to collect recent AI news, organize it across defined categories, and output a Feishu-ready daily report directly in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The self-hosted Feishu webhook example may expose a public endpoint without effective request authentication, allowing outsiders to trigger paid AI calls.

Mitigation: Add Feishu signature verification, timestamp and nonce replay checks, schema validation, and rate limits before using the webhook in a shared or enterprise bot.

Risk: Chat data used to generate reports may be sent to external AI providers during deployment.

Mitigation: Define clear data handling rules, configure approved AI providers, and avoid sending sensitive group-chat content unless the deployment policy permits it.

Risk: Unpinned dependencies in the deployment example can make runtime behavior harder to reproduce or audit.

Mitigation: Pin and review dependencies for any self-hosted deployment before installation.

## Reference(s):

- [AI Daily Report Source List](artifact/references/sources.md)
- [AI Daily Report Deployment Guide](artifact/deploy-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/c1028874817-beep/skills/ai-daily-report-1)
- [OpenAI Blog](https://openai.com/blog)
- [Google AI Blog](https://ai.googleblog.com)
- [Microsoft AI Blog](https://blogs.microsoft.com/ai)
- [Feishu Open Platform Documentation](https://open.feishu.cn/document)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or Feishu rich_text-ready message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Direct conversation output; no documents or disk files are produced by the skill.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
