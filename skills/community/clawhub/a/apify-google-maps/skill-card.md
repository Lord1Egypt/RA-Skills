## Description: <br>
This skill helps agents run the futurizerush Apify Google Maps Scraper actor to collect Google Maps business listings, contact details, ratings, opening hours, and optional emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and go-to-market users use this skill to start and poll Apify actor runs for Google Maps searches, then retrieve structured business listing data for enrichment, lead research, or local market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches and scraped results are processed by Apify. <br>
Mitigation: Use the skill only for data suitable for Apify processing and review the remote actor before sensitive or large jobs. <br>
Risk: The skill requires APIFY_API_TOKEN. <br>
Mitigation: Treat APIFY_API_TOKEN as a secret and avoid logging or sharing it. <br>
Risk: The skill may collect business emails by default. <br>
Mitigation: Disable scrapeEmails unless the user explicitly requests email collection and has a compliant reason to collect contact data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/apify-google-maps) <br>
- [Apify actor page](https://apify.com/futurizerush/google-maps-scraper?fpr=rush) <br>
- [Apify API docs](https://docs.apify.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and bash examples plus JSON result schemas.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_API_TOKEN; output may include business contact data and emails when scrapeEmails is enabled.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
