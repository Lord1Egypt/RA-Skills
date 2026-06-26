## Description: <br>
爬取抖音爆款视频和文案数据，使用 Playwright 自动化浏览器操作，支持搜索关键词、获取热榜、提取视频信息和文案等功能。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to search Douyin by keyword or hot-list category and collect public video metadata into terminal output or local JSON/CSV files for learning and research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated collection from Douyin may raise platform-terms, legal, copyright, privacy, or retention issues. <br>
Mitigation: Review the applicable obligations before collecting or sharing results, and use the skill only for allowed purposes. <br>
Risk: Browser automation with high request volume or logged-in sessions can trigger account or IP enforcement. <br>
Mitigation: Keep limits and delays conservative, avoid logging into Douyin in the automated browser, and stop if the site blocks or challenges requests. <br>
Risk: Saved output files may contain collected metadata and links from Douyin. <br>
Mitigation: Choose output paths deliberately and apply appropriate access controls and retention rules. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/douyin-search-scraper) <br>
- [Skill README](artifact/README.md) <br>
- [Playwright Documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Terminal text plus optional JSON or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include video metadata such as title, author, engagement counts, URL, tags, and publish time; result count is controlled by the command limit.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
