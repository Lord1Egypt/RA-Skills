## Description:

通过官方 Gecho Bridge MCP 按关键词搜索 Facebook Reels，返回排序后的视频、互动数据、详情、评论和链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, marketers, and social-media operators use this skill to ask an agent for keyword-based Facebook Reels research through Gecho Bridge. It is intended for collecting and summarizing ranked Reels results, interaction metrics, details, comments, links, and optional saved result paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a logged-in Facebook browser session connected through the Gecho Chrome extension and MCP bridge.

Mitigation: Install and use it only when comfortable with that setup, keep login and verification steps under user control in Chrome, and stop if Facebook presents a blocking prompt.

Risk: Saved result files can retain social-media data from Facebook Reels research.

Mitigation: Choose save directories deliberately, avoid saving data that is not needed, and remove retained files when the research task is complete.

Risk: Platform prompts, timeouts, or enrichment failures can produce empty or partial results.

Mitigation: Report empty, timed-out, failed, or partial states plainly and avoid presenting incomplete details as complete results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/facebook-reels-search-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional inline shell commands, structured result summaries, and local save paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize the most useful returned videos and report partial results or save failures when the MCP workflow cannot complete every enrichment step.]

## Skill Version(s):

1.1.38 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
