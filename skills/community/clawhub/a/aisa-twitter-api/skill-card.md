## Description: <br>
Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts after the user completes OAuth in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisapay](https://clawhub.ai/user/aisapay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Twitter/X data, monitor social activity, inspect profiles and trends, and publish posts after completing OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish publicly to Twitter/X. <br>
Mitigation: Verify the final text, media files, and whether the action is standalone, quote, reply, or threaded before posting. <br>
Risk: Command output can expose the raw AISA_API_KEY. <br>
Mitigation: Treat command output as sensitive and avoid sharing logs that include credential values. <br>
Risk: Changing TWITTER_RELAY_BASE_URL can route requests through an alternate relay. <br>
Mitigation: Leave TWITTER_RELAY_BASE_URL unset unless the alternate relay is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/aisapay/aisa-twitter-api) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [OpenClaw Twitter OAuth](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and Python 3; posting actions require user OAuth authorization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
