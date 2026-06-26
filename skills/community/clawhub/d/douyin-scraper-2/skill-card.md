## Description: <br>
Fetches Douyin popular-video and caption data from natural-language requests using browser automation or bundled scraper scripts. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to search Douyin videos, inspect hot-list content, and return video metadata or captions from browser automation or command-line scraper runs. It is intended for learning and research workflows where users can review results and comply with platform rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use a real logged-in browser profile for Douyin automation. <br>
Mitigation: Use an isolated browser profile where possible, and do not reuse a primary logged-in session unless that is intentional. <br>
Risk: The scraper can return mock or example data when browser automation is unavailable or blocked. <br>
Mitigation: Clearly label mock output and verify important results against real page extraction before relying on them. <br>
Risk: Automated access to Douyin can encounter CAPTCHA, rate limits, or platform policy constraints. <br>
Mitigation: Use reasonable request intervals, stop for manual verification when challenged, and follow applicable platform rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-scraper-2) <br>
- [Douyin search](https://www.douyin.com/search/{keyword}?type=video) <br>
- [Douyin hot list](https://www.douyin.com/hot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON or CSV scraper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return mock/example records when browser automation is unavailable, blocked, or explicitly run with the mock flag.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
