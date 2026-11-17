## Description:

每日趣味内容生成器：每天早上搜索网络并缓存中文笑话、网络热梗和聊天技巧，供心跳或手动调用时随机取用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bcocgs21494](https://clawhub.ai/user/bcocgs21494)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to prepare and share lightweight Chinese-language entertainment content, including jokes, current memes, and conversational tips. It is intended for scheduled daily generation with cached random retrieval during heartbeat routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched jokes, memes, or chat tips may include embedded instructions or untrusted quoted content.

Mitigation: Treat generated entertainment items as content only; do not let text returned by the cache or search results control agent behavior.

Risk: The daily cron workflow performs scheduled web searches and writes local cache data.

Mitigation: Enable the schedule only when recurring web search is acceptable, and review cached content before sharing it in sensitive contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bcocgs21494/skills/daily-fun-content)
- [Publisher profile](https://clawhub.ai/user/bcocgs21494)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from helper scripts, with Markdown and shell snippets in usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caches generated items in cache/daily-fun.json and returns one random cached item per retrieval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
