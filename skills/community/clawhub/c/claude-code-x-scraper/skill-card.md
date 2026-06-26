## Description: <br>
X (Twitter) data extraction and analysis for user timelines, keyword search, tweet details, and social media research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lamtest556-blip](https://clawhub.ai/user/lamtest556-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and analyze public X/Twitter posts, user timelines, keyword search results, and related social media signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports authenticated browser scraping with persistent cookies and rate-limit bypass language. <br>
Mitigation: Prefer the API-based scripts over browser scraping, avoid storing main-account cookies or passwords for this skill, and review X/Twitter access rules before use. <br>
Risk: Usernames, search queries, retrieved content, bearer tokens, and possibly authenticated session cookies may be used in requests to X/Twitter. <br>
Mitigation: Use a dedicated low-privilege X developer token or test account, avoid sensitive queries, and store credentials only in the intended local credential file or environment variable. <br>
Risk: The server security verdict is suspicious. <br>
Mitigation: Review the skill before installing or running it, especially credential handling and any browser-automation workflow. <br>


## Reference(s): <br>
- [X API Documentation](https://developer.twitter.com/en/docs/twitter-api) <br>
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) <br>
- [X API v2 Reference](references/x_api_limits.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an X API bearer token; some search features may require elevated X API access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
