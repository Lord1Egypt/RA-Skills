## Description: <br>
Guides agents through collecting TikTok post comments and threaded replies with the futurizerush Apify TikTok comment scraper actor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futurizerush](https://clawhub.ai/user/futurizerush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to start Apify runs for public TikTok posts, poll for completion, and retrieve comment and reply datasets for engagement analysis or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok URLs and scraped comment or profile metadata are sent to Apify and the named third-party actor. <br>
Mitigation: Use only when that third-party data flow is acceptable, avoid adding sensitive context to requests, and review the actor's pricing and trustworthiness before use. <br>
Risk: Apify API tokens can authorize account activity if exposed. <br>
Mitigation: Store APIFY_API_TOKEN in a secret store or environment manager and do not paste it into shared logs, prompts, or files. <br>
Risk: Collected datasets may retain comment and profile metadata after the agent finishes its task. <br>
Mitigation: Review and clean up Apify datasets when the extracted data is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futurizerush/apify-tiktok-comments) <br>
- [Publisher profile](https://clawhub.ai/user/futurizerush) <br>
- [Apify actor page](https://apify.com/futurizerush/tiktok-comment-scraper?fpr=rush) <br>
- [Apify API documentation](https://docs.apify.com/api/v2) <br>
- [Apify API token settings](https://console.apify.com/account/integrations?fpr=rush) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash examples plus JSON result schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_API_TOKEN and sends TikTok URLs to Apify for asynchronous actor runs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
