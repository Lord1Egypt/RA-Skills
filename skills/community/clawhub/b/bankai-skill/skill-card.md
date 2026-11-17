## Description:

银行AI写作助手——一句话需求即生成59种"银行味"公文底稿，严格遵循GB/T 9704-2012格式，内置反编造护栏。需自备DeepSeek API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[458468698](https://clawhub.ai/user/458468698)

### License/Terms of Use:

MIT-0

## Use Case:

Banking employees and financial-services teams use this skill to turn conversational requests or structured fields into Chinese plain-text banking document drafts across regulatory replies, analysis reports, administrative documents, policies, summaries, and custom document types for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can send banking draft content and a selected environment-variable secret to a model endpoint.

Mitigation: Use a dedicated DeepSeek or private-model API key, avoid pointing --key-env at unrelated secrets, and approve the endpoint before installation.

Risk: Customer, account, regulatory, or confidential banking content may be exposed if public-model routing is used without approval.

Mitigation: Route sensitive use cases through an approved private or internal OpenAI-compatible endpoint, or obtain organizational approval before using the public DeepSeek endpoint.

Risk: Generated banking drafts may contain placeholders or content that still needs validation.

Mitigation: Require human compliance review, fill all XX placeholders from verified sources, and do not submit generated drafts directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/458468698/skills/bankai-skill)
- [BankAI homepage](https://www.deepwater84.cn/bankai/)
- [BankAI usage and operations guide](references/usage.md)
- [BankAI scenario catalog](references/scenarios.mjs)
- [DeepSeek platform](https://platform.deepseek.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text banking document drafts with optional CLI output and concise setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated drafts use XX placeholders for missing facts and are intended for human compliance review before use.]

## Skill Version(s):

1.0.1 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
