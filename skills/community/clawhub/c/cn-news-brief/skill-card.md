## Description: <br>
Cn News Brief fetches public Chinese trending-news feeds and formats a concise categorized news brief in Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who want a brief Chinese-language news snapshot use this skill to fetch public trending topics from Baidu, Weibo, and Zhihu, classify them by category, and return a concise daily brief. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public Baidu, Weibo, and Zhihu endpoints to retrieve trending-news data. <br>
Mitigation: Run it only where those public network requests are acceptable, and review network policy before deployment. <br>
Risk: Trending feeds can be incomplete, unavailable, or change format, which may produce missing or misleading brief items. <br>
Mitigation: Verify important news against primary sources before using the brief for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-news-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands] <br>
**Output Format:** [Plain text or Markdown-style news brief, with optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can filter by category, limit item count, and emit JSON for downstream processing.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
