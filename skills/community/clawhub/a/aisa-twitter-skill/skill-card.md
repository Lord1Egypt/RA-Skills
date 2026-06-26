## Description: <br>
Searches and reads X (Twitter) profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and publishes posts after the user completes OAuth in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowen-dotcom](https://clawhub.ai/user/bowen-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search, monitor, and analyze Twitter/X data and to publish text, image, video, quote, reply, and threaded posts through AIsa-backed API and OAuth workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AISA_API_KEY may be exposed in normal command output, shared terminals, logs, or agent transcripts. <br>
Mitigation: Run authorize, post, and status commands only in trusted sessions and redact AISA_API_KEY before sharing logs or transcripts. <br>
Risk: OAuth-backed posting can publish content through the authorized Twitter/X account. <br>
Mitigation: Confirm the target account, post text, relationship mode, and media before running post commands; treat authorization links as granting posting authority. <br>
Risk: Uploaded media may become public when posted to Twitter/X. <br>
Mitigation: Attach only local files the user explicitly intends to publish and do not synthesize captions or duplicate single attachments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bowen-dotcom/aisa-twitter-skill) <br>
- [OpenClaw Twitter OAuth posting guide](references/post_twitter.md) <br>
- [AIsa API reference](https://docs.aisa.one/reference/) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API responses] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; posting requires browser OAuth authorization and may return authorization links, tweet IDs, tweet links, or API error payloads.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
