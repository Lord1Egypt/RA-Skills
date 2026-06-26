## Description: <br>
Fetches the latest cryptocurrency, Web3, and AI industry news from BlockBeats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuzipeng](https://clawhub.ai/user/xuzipeng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current BlockBeats crypto, Web3, and AI news, optionally filtered by category, result count, and page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to the BlockBeats API using a user-provided API key. <br>
Mitigation: Use a dedicated, revocable BlockBeats API key and avoid exposing unrelated secrets in the runtime environment. <br>
Risk: Returned news content may be incomplete, stale, or unavailable if the external API fails or filtering parameters are too narrow. <br>
Mitigation: Check command errors and adjust NEWS_SIZE, NEWS_PAGE, or NEWS_TYPE when expected items are missing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuzipeng/crypto-news) <br>
- [BlockBeats Open Flash API](https://api.theblockbeats.news/v1/open-api/open-flash) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration] <br>
**Output Format:** [Markdown news items printed by a Node.js command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and BLOCKBEATS_API_KEY. Optional NEWS_SIZE, NEWS_PAGE, and NEWS_TYPE environment variables select result count, page, and category.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
