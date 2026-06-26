## Description: <br>
Guides agents through using Apify's Threads Replies Scraper actor to collect public replies and comments from Meta Threads posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect public Threads post replies with an Apify actor, poll asynchronous runs, and work with the returned JSON for conversation analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Threads URLs and scraped results are processed and stored by Apify, and the third-party actor may affect account cost or data handling. <br>
Mitigation: Use a scoped or dedicated Apify token, verify target URLs before running, and review the actor's handling and cost profile for your account. <br>
Risk: Invalid input format, unavailable posts, or private posts can cause failed runs or incomplete collection. <br>
Mitigation: Use public Threads post URLs in requestListSources format, keep max_replies within the documented range, and handle failed Apify run statuses before using results. <br>


## Reference(s): <br>
- [Apify Threads Replies Scraper actor](https://apify.com/futurizerush/threads-replies-scraper?fpr=rush) <br>
- [Apify API v2 documentation](https://docs.apify.com/api/v2) <br>
- [Apify account integrations](https://console.apify.com/account/integrations?fpr=rush) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash examples plus JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_API_TOKEN; fetched results are JSON arrays from Apify datasets.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
