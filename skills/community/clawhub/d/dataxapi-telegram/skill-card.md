## Description:

Public Telegram data through DataXAPI: channels, messages. 3 endpoints, $0.0020 a call, a failed call is free. Use when the user asks about Telegram content, accounts, comments or trends, or gives a Telegram link, ID or account name. 通过 DataXAPI 取Telegram的公开数据：频道、消息。3 个接口，一次 $0.0020，失败不收费。用户问到Telegram的内容、账号、评论或热点，或给出Telegram的链接、编号、账号名时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for public Telegram channel details, recent posts, or a specific message. The agent can look up matching endpoints and prices, then summarize returned data with its DataXAPI source and retrieval time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback searches may send the user's wording to DataXAPI, potentially exposing sensitive text.

Mitigation: Explain this before searching, minimize or redact sensitive wording, and search only when the user is comfortable with the disclosure.

Risk: The suggested CLI commands do not pin a package version.

Mitigation: Pin and review the CLI package version before installing or running it.

Risk: The security scan is partial and unresolved local references leave evidence incomplete.

Mitigation: Review the complete installed skill and resolve referenced local files before relying on the scan assessment.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [Telegram API documentation](https://dataxapi.com/apis/telegram/)
- [Telegram API pricing](https://dataxapi.com/pricing/telegram/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Natural-language summaries with structured JSON API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Telegram data; API calls are billed per call, with additional pages charged separately.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
