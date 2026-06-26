## Description: <br>
Uses fapi.uk's Reddit REST API to query users, subreddits, searches, and post details from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huojiecs110](https://clawhub.ai/user/huojiecs110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to retrieve and summarize Reddit user activity, subreddit posts, search results, and post details through fapi.uk without manually assembling REST parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expose billable fapi.uk API credentials or auth tokens by pasting them into chat. <br>
Mitigation: Store credentials in OpenClaw configuration or a secure secret store, use revocable keys with spending limits, and rotate any credential already shared in a transcript. <br>
Risk: Reddit API calls through fapi.uk may consume account credits. <br>
Mitigation: Check account balance before use and stop requests when credits are insufficient. <br>


## Reference(s): <br>
- [Fapi Reddit on ClawHub](https://clawhub.ai/huojiecs110/fapi-reddit) <br>
- [fapi.uk](https://fapi.uk) <br>
- [fapi.uk API documentation](https://utools.readme.io) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Text, Configuration] <br>
**Output Format:** [Markdown and natural-language summaries with optional JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw configuration commands and Reddit API request guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
