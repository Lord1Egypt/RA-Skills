## Description: <br>
Search X (Twitter) data using Felo X Search API for user lookup, user search, user tweets, tweet search, and tweet replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve public X/Twitter users, tweets, timelines, search results, and replies through the Felo API. It is useful when an agent needs structured social search results and readable summaries instead of general web search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: X/Twitter search terms, usernames, tweet IDs, and related parameters are sent to Felo's external API. <br>
Mitigation: Use only when third-party transmission is permitted; avoid secrets, regulated data, or sensitive investigations unless organizational policy allows it. <br>
Risk: The skill requires a Felo API key in the FELO_API_KEY environment variable. <br>
Mitigation: Store the API key as a secret, avoid placing it in prompts or command history, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [Felo X Search API](https://openapi.felo.ai/docs/api-reference/v2/x-search.html) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>
- [Felo X Search on ClawHub](https://clawhub.ai/wangzhiming1999/felo-x-search) <br>
- [Publisher Profile](https://clawhub.ai/user/wangzhiming1999) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Readable Markdown by default, raw JSON when requested, and shell commands or environment configuration for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FELO_API_KEY; supports pagination cursors, result limits, time filters, raw JSON output, request timeout control, and optional FELO_API_BASE override.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
