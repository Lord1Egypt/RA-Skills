## Description:

Fetches the latest cryptocurrency, Web3, and AI industry news from BlockBeats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuzipeng](https://clawhub.ai/user/xuzipeng)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve current BlockBeats flash news about cryptocurrency, Web3, and AI, with optional filtering by category, page, and item count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BlockBeats API key and sends authenticated requests to the BlockBeats API.

Mitigation: Provide only a scoped BlockBeats API key suitable for news retrieval, store it in the BLOCKBEATS_API_KEY environment variable, and rotate or revoke it if no longer needed.

Risk: The skill is focused on Chinese-language BlockBeats flash news and may not provide complete market research coverage.

Mitigation: Treat outputs as news-fetching results from BlockBeats and corroborate important financial or market claims with additional sources before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuzipeng/skills/crypto-news)
- [Publisher profile](https://clawhub.ai/user/xuzipeng)
- [BlockBeats open flash API endpoint](https://api.theblockbeats.news/v1/open-api/open-flash)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown news items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language BlockBeats news content; category, page, and item count can be selected through NEWS_TYPE, NEWS_PAGE, and NEWS_SIZE.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
