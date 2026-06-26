## Description: <br>
帮助代理解析抖音搜索或热榜请求并运行 Playwright-based scripts, with current security evidence noting that returned video metrics and hot-list entries are synthetic placeholder data rather than verified live Douyin results. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to turn natural-language Douyin search or hot-list requests into scraper commands and readable summaries. Treat returned video data as demonstration or development output unless the implementation is changed to extract and label live page data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is framed as a Douyin scraper while security evidence says the Python and Node scripts return synthetic placeholder video data. <br>
Mitigation: Do not rely on returned metrics, authors, URLs, or hot-list entries as real Douyin evidence until the scripts extract actual page data and clearly mark mock versus live results. <br>
Risk: The scripts can launch Playwright against Douyin pages and may be affected by platform rules, rate limits, browser failures, or page changes. <br>
Mitigation: Review the target site's terms and local policy before use, keep request rates low, and validate scraper output against live page evidence before using it in decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-scraper-terry) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, CSV files, guidance] <br>
**Output Format:** [Markdown or terminal text with optional JSON/CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and hot-list commands accept keyword, category, limit, output path, and json/csv format options.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
