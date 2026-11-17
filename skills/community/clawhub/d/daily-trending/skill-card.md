## Description:

Daily Trending fetches Chinese hot-topic lists from tophub.today and returns a concise set of factual daily headlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enchograph](https://clawhub.ai/user/enchograph)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to get a short Chinese-language summary of the day's most relevant hot topics across TopHub sources such as Zhihu, Weibo, Baidu, 36Kr, Huxiu, The Paper, 52pojie, and Hupu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch public tophub.today pages whose rankings and availability change over time.

Mitigation: Treat the output as a current snapshot and verify important news separately before relying on it.

Risk: The skill's requested output omits source labels, which can make individual headlines harder to trace.

Mitigation: For important topics, ask the agent to verify the item against the original publisher or another reliable source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enchograph/skills/daily-trending)
- [Publisher profile](https://clawhub.ai/user/enchograph)
- [TopHub Weibo hot search](https://tophub.today/n/KqndgxeLl9)
- [TopHub Zhihu hot list](https://tophub.today/n/mproPpoq6O)
- [TopHub Baidu real-time hot topics](https://tophub.today/n/Jb0vmloB1G)
- [TopHub 36Kr 24-hour list](https://tophub.today/n/Q1Vd5Ko85R)
- [TopHub Huxiu hot articles](https://tophub.today/n/5VaobgvAj1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style numbered list in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns five selected headlines and omits source labels by design.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
