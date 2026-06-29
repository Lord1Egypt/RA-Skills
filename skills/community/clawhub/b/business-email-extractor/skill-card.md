## Description: <br>
Extract verified business email addresses from Google Maps listings for a chosen industry and location, with filtering guidance for outreach-ready contact lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmapsscraper](https://clawhub.ai/user/gmapsscraper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, and business-development users use this skill to identify publicly listed business email addresses for targeted B2B outreach and to prepare a filtered CSV contact list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business search targets and extraction requests are sent to the third-party gmapsscraper.io API. <br>
Mitigation: Use only with approval to share those targets with the service, and protect the API key through environment variables rather than hard-coding it. <br>
Risk: Harvested email lists may contain personal data or be subject to outreach, privacy, and opt-out requirements. <br>
Mitigation: Confirm the intended outreach complies with applicable email and privacy rules, include unsubscribe handling, and honor opt-out requests promptly. <br>
Risk: The skill saves extracted email data to local CSV files. <br>
Mitigation: Store CSV outputs in approved locations, restrict access, and delete data when it is no longer needed. <br>


## Reference(s): <br>
- [GMaps Scraper](https://gmapsscraper.io) <br>
- [Business Email Extractor on ClawHub](https://clawhub.ai/gmapsscraper/business-email-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown with bash commands and CSV file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GMAPS_SCRAPER_API_KEY and curl; outputs a locally saved CSV of extracted emails with quality guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
