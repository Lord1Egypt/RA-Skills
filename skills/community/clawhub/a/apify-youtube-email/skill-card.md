## Description: <br>
Helps agents run the futurizerush Apify actor to find public email addresses and contact details from YouTube channels by keyword or channel URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, growth teams, and agent operators use this skill to start and monitor Apify runs, then retrieve JSON contact results for lawful, consent-aware influencer outreach or lead research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a third-party Apify actor and an Apify token to collect public YouTube contact data. <br>
Mitigation: Install only if that third-party processing is acceptable, keep searches narrow, and review Apify dataset retention. <br>
Risk: Collected email addresses may create privacy, platform-terms, or anti-spam compliance obligations. <br>
Mitigation: Use results only for lawful, consent-aware outreach that respects YouTube, Apify, and anti-spam requirements. <br>
Risk: The Apify API token could be exposed through logs, shell history, or shared examples. <br>
Mitigation: Store APIFY_API_TOKEN in environment or secret storage, avoid printing it, and rotate it promptly if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/apify-youtube-email) <br>
- [Apify actor page](https://apify.com/futurizerush/youtube-email-scraper?fpr=rush) <br>
- [Apify API v2 documentation](https://docs.apify.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_API_TOKEN and returns Apify dataset items as a JSON array.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
