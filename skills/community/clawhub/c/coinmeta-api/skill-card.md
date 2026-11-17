## Description:

查询加密货币快讯。触发场景：查询币圈快讯、获取加密货币新闻、crypto news、币圈资讯。

This skill is ready for commercial/non-commercial use.

## Publisher:

[semithin](https://clawhub.ai/user/semithin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and search cryptocurrency news flashes from CoinMeta, then present titles, views, timestamps, and cleaned summaries in a readable format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a CoinMeta API key and sends crypto-news query parameters to CoinMeta.

Mitigation: Provide the API key through the COINMETA_API_KEY environment variable or a secret manager, and avoid pasting credentials into prompts, logs, or shared files.

Risk: The skill depends on CoinMeta API responses and network availability for news results.

Mitigation: Handle non-200 API codes and network errors as user-visible retry or troubleshooting guidance, and verify important crypto-news results against trusted sources before acting on them.

Risk: The skill content and expected output are primarily Chinese-language.

Mitigation: Ask the agent to translate or adapt responses when users need another language.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/semithin/skills/coinmeta-api)
- [Publisher profile](https://clawhub.ai/user/semithin)
- [CoinMeta API base URL](https://api.coinmeta.com)
- [Newsflash list endpoint](https://api.coinmeta.com/open/v1/newsflash/list)
- [Newsflash search endpoint](https://www.coinmeta.com/open/v1/newsflash/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and formatted news summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires COINMETA_API_KEY and curl; content returned by the API may contain HTML that should be stripped before display.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
