## Description: <br>
Scrapes Hacker News stories, comments, and discussions through an Apify Actor using the Apify REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcinDudekDev](https://clawhub.ai/user/MarcinDudekDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search Hacker News, collect matching stories or comments, and summarize discussion trends from Apify results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hacker News search terms and scrape parameters are sent to Apify. <br>
Mitigation: Avoid sensitive private queries and review requested scrape parameters before execution. <br>
Risk: The APIFY_TOKEN may consume Apify account quota and grants API access appropriate to that token. <br>
Mitigation: Use a limited token where possible and monitor Apify quota usage. <br>


## Reference(s): <br>
- [ClawHub listing for Apify HN Scraper](https://clawhub.ai/MarcinDudekDev/apify-hn-scraper) <br>
- [Apify Actor synchronous dataset endpoint](https://api.apify.com/v2/acts/0UDODOnpTkxY3Oc90/run-sync-get-dataset-items?token=$APIFY_TOKEN) <br>
- [Apify Actor run endpoint](https://api.apify.com/v2/acts/0UDODOnpTkxY3Oc90/runs?token=$APIFY_TOKEN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN plus curl and jq; results may include Hacker News story and comment data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
