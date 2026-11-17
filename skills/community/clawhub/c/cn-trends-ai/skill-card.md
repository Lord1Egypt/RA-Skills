## Description:

Fetches real-time Chinese trending-topic lists from Zhihu, Weibo, Baidu, and Bilibili, with optional keyword filtering and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to retrieve current Chinese trending topics across major platforms, compare popularity signals, and filter results for a keyword or topic of interest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public third-party trend platforms whose APIs may change, rate-limit requests, or become unavailable.

Mitigation: Treat empty or partial results as a normal failure mode and verify important trend findings against the source platform before relying on them.

Risk: Returned results are public, Chinese-language trending topics and may include fast-changing or platform-curated content.

Mitigation: Use the output as a current signal rather than a complete or authoritative measurement of public interest.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/freedompixels/skills/cn-trends-ai)
- [AISoBrand](https://aisobrand.com)
- [Zhihu hot list API](https://api.zhihu.com/topstory/hot-lists/total?limit=20)
- [Weibo hot search API](https://weibo.com/ajax/side/hotSearch)
- [Baidu realtime trends API](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Bilibili ranking API](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text trend report or JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language trend results; supports platform selection, per-platform limits, keyword filtering, and no persistence.]

## Skill Version(s):

1.3.2 (source: server release metadata; artifact frontmatter reports 1.3.0 and artifact skill.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
