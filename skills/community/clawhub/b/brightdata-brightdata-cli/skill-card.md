## Description: <br>
Guides agents in using the Bright Data CLI to authenticate, scrape web pages, run search queries, extract structured platform data, manage proxy zones, and check account budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to propose Bright Data CLI commands for web scraping, SERP queries, structured data extraction, account budget checks, and proxy-zone management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends a remote installer pattern that runs network code directly on the user's machine. <br>
Mitigation: Prefer npm or npx installation paths such as npm install -g @brightdata/cli or npx --yes --package @brightdata/cli before using curl-to-bash. <br>
Risk: The skill involves OAuth or API-key authentication for Bright Data account access. <br>
Mitigation: Use OAuth or device login when possible, avoid pasting API keys into commands, and protect any BRIGHTDATA_API_KEY environment value. <br>
Risk: Scraping, proxy-zone changes, and account-budget actions can affect compliance posture and spend. <br>
Mitigation: Confirm scraping targets, account budget, and proxy-zone changes are acceptable for the user's use case before running commands. <br>


## Reference(s): <br>
- [Bright Data CLI command reference](references/commands.md) <br>
- [Bright Data CLI pipeline types reference](references/pipelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command flags, environment variables, authentication options, and file output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
