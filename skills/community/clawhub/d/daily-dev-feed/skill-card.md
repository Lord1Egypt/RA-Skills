## Description: <br>
Curated developer content aggregation powered by daily.dev. Get real-time articles, trending topics, and personalized feeds from thousands of validated sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phancthanhduc](https://clawhub.ai/user/phancthanhduc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to collect current developer articles, trends, personalized feeds, bookmarks, and technology research from daily.dev. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs a daily.dev API token and can access personalized content. <br>
Mitigation: Store DAILY_DEV_TOKEN in a credential manager or environment variable, never commit it, and send it only to api.daily.dev. <br>
Risk: The skill can change daily.dev account items such as feeds, followed tags, profile-related settings, and bookmarks. <br>
Mitigation: Require user confirmation before creating feeds, following tags, editing profile-related settings, or adding bookmarks. <br>
Risk: The skill depends on the separate daily-dev skill. <br>
Mitigation: Review and install the daily-dev dependency before using this release. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/phancthanhduc/daily-dev-feed) <br>
- [daily.dev Plus subscription](https://app.daily.dev/plus) <br>
- [daily.dev API token settings](https://app.daily.dev/settings/api) <br>
- [daily.dev public OpenAPI specification](https://api.daily.dev/public/v1/docs/json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include article links, feed summaries, bookmarks, tag-following recommendations, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
