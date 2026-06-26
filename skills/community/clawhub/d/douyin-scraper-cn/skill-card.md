## Description: <br>
爬取抖音爆款视频和文案数据。支持自然语言搜索（如"搜索一下海鲜视频"）和结构化 CLI 调用，使用 Playwright 自动化浏览器，无浏览器时自动降级为模拟数据。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Douyin videos or hot lists from Chinese natural-language requests or structured CLI commands, then export video metadata and copywriting examples as JSON or CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may output simulated video data while presenting it as scraped Douyin results. <br>
Mitigation: Treat JSON and CSV output as examples unless real page extraction has been verified for the requested run. <br>
Risk: Automated Douyin browsing may trigger platform controls or conflict with platform rules. <br>
Mitigation: Get explicit user confirmation before running searches or hot-list collection, avoid login flows, and use conservative request pacing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-scraper-cn) <br>
- [Playwright documentation](https://playwright.dev/) <br>
- [README](README.md) <br>
- [SKILL](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, shell commands, guidance] <br>
**Output Format:** [Console text with optional JSON or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return simulated example data when Playwright is unavailable or real page extraction is not implemented.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
