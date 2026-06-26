## Description: <br>
爬取抖音搜索结果和热榜数据，使用 Playwright 自动化浏览器操作，支持自然语言搜索、关键词搜索、获取热榜和提取视频信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Douyin by natural-language or keyword prompts, retrieve hot-list entries, and export public video metadata for analysis or workflow handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation that visits Douyin may trigger anti-bot checks, CAPTCHA, platform-rate limits, or IP blocking. <br>
Mitigation: Use the skill only for explicit Douyin search or hot-list requests, keep result limits modest, add delays between requests, and stop when anti-bot controls appear. <br>
Risk: Using a logged-in personal account during scraping could expose the account to platform risk controls. <br>
Mitigation: Run the skill without logging into personal Douyin accounts. <br>
Risk: Rendered-page extraction may return incomplete or stale results if Douyin changes its page structure or blocks the request. <br>
Mitigation: Treat returned metadata as best-effort public web data and verify important results against Douyin before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-search-v2) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>
- [Playwright documentation](https://playwright.dev/) <br>
- [Douyin web search](https://www.douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, CSV, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scraper results can be emitted as JSON or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result fields include title, description, author, counts, URL, tags, and publish time when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
