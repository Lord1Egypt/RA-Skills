## Description: <br>
爬取抖音爆款视频和文案数据，使用 Playwright 自动化浏览器操作，支持搜索关键词、获取热榜、提取视频信息和文案等功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Douyin content, retrieve hot-list entries, and export video metadata and copywriting candidates for analysis or downstream content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use logged-in browser sessions or cookie files for Douyin scraping, creating account, privacy, and platform-policy exposure. <br>
Mitigation: Run only with explicit authorization, avoid cookie files or logged-in sessions unless required, store cookies as secrets, and remove them after use. <br>
Risk: The scraper can make live browser requests to Douyin and save scraped results locally. <br>
Mitigation: Use conservative limits and delays, confirm the activity complies with applicable laws and platform rules, and review saved JSON or CSV files before sharing. <br>
Risk: When Playwright is unavailable, CAPTCHA appears, or extraction fails, the artifact may return mock data. <br>
Mitigation: Check whether output is marked as simulated or mock data and verify important results against the live source before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/terrycarter1985/douyin-scraper-v3) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands; scraper outputs can be printed text, JSON, or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and hot-list commands accept keyword, category, limit, output path, and json/csv format options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
