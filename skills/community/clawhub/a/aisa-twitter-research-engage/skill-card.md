## Description: <br>
Search X/Twitter profiles, tweets, trends, and OAuth-gated posting through AIsa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to research X/Twitter accounts, tweets, trends, and conversations, then perform approved posting or engagement actions through AIsa-backed clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required AIsa API key may appear in normal command output. <br>
Mitigation: Avoid shared terminals, CI logs, and saved transcripts for status, authorize, or post commands; redact exposed keys and rotate them if disclosure occurs. <br>
Risk: The skill can post, like, follow, and unfollow on live X/Twitter accounts. <br>
Mitigation: Confirm the target account, content, and action before executing commands, and do not claim success until the API response confirms it. <br>
Risk: Tweet text and local media files are sent through AIsa-backed services for posting workflows. <br>
Mitigation: Install only when the operator trusts AIsa with the API key, tweet text, media files, and resulting live account actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/aisa-twitter-research-engage) <br>
- [AIsa publisher profile](https://clawhub.ai/user/aisadocs) <br>
- [Twitter OAuth posting workflow](artifact/references/post_twitter.md) <br>
- [Twitter engagement workflow](artifact/references/engage_twitter.md) <br>
- [AIsa API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authorization links, status summaries, tweet or profile research results, and confirmed action results after API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
