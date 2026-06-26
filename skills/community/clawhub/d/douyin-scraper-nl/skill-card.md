## Description: <br>
Douyin Scraper helps agents turn Chinese natural-language requests into Douyin keyword or hot-list scraping commands and return video metadata as JSON, CSV, or readable text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to search Douyin topics, inspect hot-list style results, and export video metadata for downstream content research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers may start browser scraping when the user intended only discussion or planning. <br>
Mitigation: Prefer explicit commands for scraping actions and confirm the target query, limit, and output path before running browser automation. <br>
Risk: Setup and execution can install browser dependencies, open Chromium, contact Douyin, and write result files. <br>
Mitigation: Install and run in an isolated workspace, review commands before execution, and keep output paths explicit. <br>
Risk: Returned rows may be mock data or unverified live page data. <br>
Mitigation: Treat results as unverified unless the output clearly shows live source data, and check the mock=true flag before using results in downstream work. <br>
Risk: Using a logged-in personal Douyin session for scraping can create account, privacy, or platform-policy exposure. <br>
Mitigation: Avoid personal logged-in sessions unless the operator understands the risks and complies with applicable platform rules and local requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/douyin-scraper-nl) <br>
- [Playwright Documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, shell commands, guidance] <br>
**Output Format:** [Readable console summaries with optional JSON or CSV result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may be live Douyin page data or mock fallback rows marked with mock=true.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
