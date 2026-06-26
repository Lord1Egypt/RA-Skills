## Description: <br>
B站自动化 - 观看视频、提取字幕、总结内容. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxsuki](https://clawhub.ai/user/maxsuki) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to search Bilibili videos, play selected videos, extract subtitles or danmaku, summarize content, and fetch video metadata through a local BrowserWing service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Bilibili actions through local BrowserWing scripts that are not included in the artifact for review. <br>
Mitigation: Install only when you trust the local BrowserWing service and the bilibili-search, bilibili-subtitle, and bilibili-info scripts it runs. <br>
Risk: Optional Bilibili session cookies can expose account access if shared or logged insecurely. <br>
Mitigation: Use BILIBILI_SESSDATA and BILIBILI_BILI_JCT only when login is required, treat them like passwords, and rotate the session if exposed. <br>
Risk: Frequent automated requests may violate Bilibili rules or trigger rate limits. <br>
Mitigation: Keep request rates low, follow Bilibili rules, and use the artifact guidance to wait between requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxsuki/bilibili-automation) <br>
- [Bilibili](https://www.bilibili.com) <br>
- [BrowserWing local API docs](http://localhost:8080/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with curl examples and structured text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and BROWSERWING_URL; optional Bilibili session cookie variables enable logged-in behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
