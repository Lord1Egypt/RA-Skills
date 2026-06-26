## Description: <br>
Apify Scraper helps agents scrape content from bot-resistant sites such as Twitter/X threads, Reddit, LinkedIn, YouTube comments, Google search results, Amazon, and Product Hunt when standard fetching is blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research agents use this skill to run Apify actors for structured scraping tasks when normal web fetch or search tools cannot retrieve full threads, comments, profiles, or search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Apify API key and sends scraping jobs to Apify infrastructure. <br>
Mitigation: Use an Apify key approved for agent use, avoid sharing unnecessary secrets, and confirm the account is acceptable for the data being scraped. <br>
Risk: Apify actor runs can consume paid credits and create datasets. <br>
Mitigation: Monitor Apify billing and datasets, set conservative item limits, and use the skill only when standard fetch or search tools are blocked. <br>
Risk: Some scraping targets, including LinkedIn, may have terms-of-service constraints. <br>
Mitigation: Scrape only sites where the intended use is authorized and apply extra review before using ToS-sensitive actors. <br>
Risk: The release depends on a referenced Apify helper script. <br>
Mitigation: Confirm the helper script is trusted or replace it with a reviewed local equivalent before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/apify-scraper) <br>
- [Apify Console](https://console.apify.com) <br>
- [Apify Billing](https://console.apify.com/billing) <br>
- [Apify API endpoint](https://api.apify.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with shell commands and JSON actor input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and APIFY_API_KEY; Apify actors return results as datasets after polling.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
