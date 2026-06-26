## Description: <br>
抓取主流中外 AI 资讯源生成中文 markdown 日报。用户说"生成今日 AI 日报"/"今天有什么 AI 新闻"等指令时启用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yan1sanjin](https://clawhub.ai/user/yan1sanjin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch public AI news sources, filter and deduplicate items, translate or summarize them in Chinese, and write a local daily Markdown digest. It supports region-aware source selection for international or China-network usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install documentation promotes running mutable remote shell or PowerShell scripts directly. <br>
Mitigation: Prefer ClawHub/openclaw installation or manually copy an inspected SKILL.md; if using remote scripts, download, inspect, and verify them before execution. <br>
Risk: The skill fetches public websites and creates or updates local digest files. <br>
Mitigation: Review the generated digest and source links before relying on it, and specify path or mode when you need to control file writes. <br>
Risk: Public news sources can be unavailable, blocked, or misleading. <br>
Mitigation: Use the region parameter for local network conditions and rely on the built-in source-rating, verification, and failure-note workflow described in the artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yan1sanjin/ai-news-digest-cn) <br>
- [README](README.md) <br>
- [Example outputs](examples/README.md) <br>
- [Hacker News](https://news.ycombinator.com/) <br>
- [Latent Space RSS](https://www.latent.space/feed) <br>
- [Anthropic News](https://www.anthropic.com/news) <br>
- [Hugging Face Blog](https://huggingface.co/blog) <br>
- [量子位](https://www.qbitai.com/) <br>
- [机器之心](https://www.jiqizhixin.com/) <br>
- [智东西](https://zhidx.com/) <br>
- [雷峰网 AI 频道](https://www.leiphone.com/category/ai) <br>
- [InfoQ 中国 AI 频道](https://www.infoq.cn/topic/AI) <br>
- [36 氪 AI 频道](https://36kr.com/information/AI/) <br>
- [钛媒体](https://www.tmtpost.com/) <br>
- [品玩](https://www.pingwest.com/) <br>
- [虎嗅前沿科技频道](https://www.huxiu.com/channel/105.html) <br>
- [TechCrunch AI](https://techcrunch.com/category/artificial-intelligence/) <br>
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence) <br>
- [One Useful Thing](https://www.oneusefulthing.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily digest file with Chinese summaries, source links, credibility labels, trend themes, fetch-failure notes, and a short confirmation message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to a local date-based path by default; supports custom path, update, snapshot, skip, and region modes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
