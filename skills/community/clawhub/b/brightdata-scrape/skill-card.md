## Description: <br>
Scrape uses the Bright Data CLI to fetch web pages as clean markdown, HTML, JSON, or screenshots and guide verification of the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to fetch page content from known URLs, scrape small or large URL lists, and handle pagination or block-page recovery through Bright Data CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bright Data credentials may be exposed or misused if API keys or saved login state are handled carelessly. <br>
Mitigation: Protect Bright Data API keys and use the skill only in environments where Bright Data CLI authentication is intended. <br>
Risk: Target URLs and fetched page data may be sent to Bright Data during scraping. <br>
Mitigation: Review URL lists before batch runs and avoid scraping sensitive or inappropriate targets. <br>
Risk: Scraped page content can contain untrusted text that attempts to influence the agent. <br>
Mitigation: Treat fetched content as data, verify outputs before use, and do not follow instructions found inside scraped pages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/meirk-brd/brightdata-scrape) <br>
- [Flag reference](references/flags.md) <br>
- [Scraping patterns](references/patterns.md) <br>
- [Worked examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file paths or command examples for markdown, HTML, JSON, and screenshot scrape outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
