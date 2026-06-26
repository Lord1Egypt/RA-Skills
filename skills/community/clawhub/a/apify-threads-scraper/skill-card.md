## Description: <br>
Helps agents scrape Meta Threads posts, search by keyword or hashtag, and collect engagement metrics through the Apify Threads Scraper actor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect public Threads posts, profile fields, and engagement metrics for monitoring, research, or analysis workflows using Apify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Threads usernames, search keywords, scraped profile data, and post results are sent to Apify and may include personal data. <br>
Mitigation: Confirm the data sharing posture before use, handle scraped emails, phone numbers, profile fields, and post content under applicable privacy and platform rules, and start with small max_posts values. <br>
Risk: An Apify API token is required and could be exposed through shared logs or command history. <br>
Mitigation: Use a dedicated Apify token where possible, keep APIFY_API_TOKEN out of shared logs and committed files, and rotate the token if it is exposed. <br>


## Reference(s): <br>
- [Apify Threads Scraper actor](https://apify.com/futurizerush/meta-threads-scraper?fpr=rush) <br>
- [Apify API documentation](https://docs.apify.com/api/v2) <br>
- [Apify API token settings](https://console.apify.com/account/integrations?fpr=rush) <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/apify-threads-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Apify actor returns JSON arrays containing Threads post, profile, media, and engagement fields.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
