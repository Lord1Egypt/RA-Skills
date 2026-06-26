## Description: <br>
Query the AI News Feed API for real-time AI/ML news from 57+ curated Twitter/X accounts, returning bilingual summaries, importance scores, topic tags, and JSON responses through RapidAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FredHJC](https://clawhub.ai/user/FredHJC) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to fetch current AI and machine-learning news, trending posts, account feeds, tags, and enriched summaries from the RapidAPI-hosted AI News Feed API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests and query parameters to an external RapidAPI-hosted service. <br>
Mitigation: Use it only when external AI news retrieval is intended, and avoid sending sensitive or private query context. <br>
Risk: A RapidAPI key is required for requests. <br>
Mitigation: Store the key in a trusted secret or environment-variable mechanism and do not paste it into public chats or files. <br>
Risk: Returned tweet timestamps are UTC. <br>
Mitigation: Convert tweetedAt values to the user's local timezone before displaying time-sensitive news. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FredHJC/ai-news-feed) <br>
- [RapidAPI listing](https://rapidapi.com/jiachenfred/api/twitter-ai-news-feed) <br>
- [API response schemas](references/api-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with inline HTTP endpoints and bash/curl examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided RapidAPI key; tweetedAt values are UTC and should be converted to the user's local timezone before display.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
