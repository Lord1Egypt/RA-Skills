## Description: <br>
Assists agents with Douyin keyword search and hot-list workflows by running scraper commands that can emit JSON or CSV video metadata. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language Douyin search or hot-list requests into runnable scraper commands and saved result files. The release should be treated as research and development evidence because the package itself says it is for learning or research and the security summary reports simulated results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release may present invented sample data as scraped Douyin results. <br>
Mitigation: Treat JSON and CSV outputs as mock data unless the publisher supplies verified extraction behavior and clearly labels simulated output. <br>
Risk: Collected creator or content metadata may trigger platform-rule, privacy, or local-law obligations. <br>
Mitigation: Check Douyin terms, privacy requirements, and applicable law before saving, sharing, or relying on metadata. <br>
Risk: Automated browser access can fail or degrade to simulated data. <br>
Mitigation: Review stderr notices and validate outputs against live sources before using the results for business or research decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-scraper-terrycarter) <br>
- [Playwright documentation](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, CSV, files, guidance] <br>
**Output Format:** [Shell command guidance with optional JSON or CSV output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result fields include title, description, author, engagement counts, URL, tags, and publish time; browser failures fall back to simulated data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
