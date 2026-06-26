## Description: <br>
Containerized Crawlee and Playwright web scraping skill for Amazon product data, YouTube transcripts, and generic dynamic pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run a Dockerized scraper for Amazon product research, YouTube transcript capture, and extraction from dynamic webpages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-operated scraping can target sites or URLs the user is not authorized to scrape. <br>
Mitigation: Use the skill only for authorized sites, verify every generated URL before execution, and avoid internal or sensitive URLs. <br>
Risk: Scraped content may be captured in logs or downstream agent context. <br>
Mitigation: Treat scraper output as potentially retained, avoid collecting sensitive data, and redact or discard sensitive output before sharing it. <br>
Risk: The browser-based scraper visits arbitrary web pages with broad scraping authority. <br>
Mitigation: Run the Docker container non-privileged, avoid host mounts, and apply network restrictions appropriate for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiafar/deep-scraper-amazon) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Docker shell commands and JSON scraper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker; generic page text is capped at 10000 characters and YouTube transcript text is capped at 15000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
