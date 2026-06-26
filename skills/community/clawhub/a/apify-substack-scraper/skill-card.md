## Description: <br>
Scrape Substack newsletters and articles through an Apify Actor using the user's APIFY_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcinDudekDev](https://clawhub.ai/user/MarcinDudekDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to run an Apify Substack scraping actor, collect article metadata or content from Substack publication URLs, and summarize or export the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Substack URLs, scrape parameters, and results are processed through Apify under the user's APIFY_TOKEN. <br>
Mitigation: Review the referenced Apify actor before use and use a minimally scoped Apify token where possible. <br>
Risk: Execution depends on APIFY_TOKEN, curl, jq, and external network access to Apify. <br>
Mitigation: Confirm the required environment variable, binaries, and network access before running the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MarcinDudekDev/apify-substack-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with bash command snippets and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN, curl, and jq; may offer JSON or CSV export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
