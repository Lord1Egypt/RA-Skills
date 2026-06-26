## Description: <br>
Helps agents search Google News through the Apify Google News Scraper actor and retrieve article metadata, summaries, and limited article content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and newsroom-adjacent teams use this skill to configure Apify runs for Google News search, monitor topics, collect recent headlines, and fetch structured article results for downstream analysis or summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Google News scraping through Apify and a named third-party actor. <br>
Mitigation: Install only if that third-party service use is acceptable, and review the actor's cost and data-retention behavior before production use. <br>
Risk: The examples include API-token authentication and show token values in request URLs. <br>
Mitigation: Use a dedicated or least-privilege Apify token where possible, and prefer header-based authentication when adapting the examples. <br>
Risk: News monitoring topics or query lists may reveal sensitive business interests or investigations. <br>
Mitigation: Avoid sensitive monitoring topics unless the agent environment and Apify account are approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/apify-google-news) <br>
- [Publisher profile](https://clawhub.ai/user/futurizerush) <br>
- [Apify Google News Scraper actor](https://apify.com/futurizerush/google-news-scraper?fpr=rush) <br>
- [Apify API documentation](https://docs.apify.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with Python and bash examples plus JSON result schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_API_TOKEN; returns Google News result arrays with article metadata, source fields, timestamps, summaries, and articleContent snippets when available.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence; artifact frontmatter is 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
