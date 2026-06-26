## Description: <br>
Interact with the AIOZ Stream API to manage videos, audio, playlists, players, webhooks, analytics, payments, chapters, and transcripts on the AIOZ decentralized streaming platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinhbui3004](https://clawhub.ai/user/vinhbui3004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and operators with AIOZ Stream accounts use this skill to prepare authenticated API calls and operational guidance for uploading media, managing streaming assets, configuring webhooks and players, and reviewing analytics or payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct broad account-changing actions in an AIOZ Stream account, including deletes and retries. <br>
Mitigation: Use limited or temporary AIOZ credentials where possible and confirm exact media, webhook, player, playlist, or key IDs before destructive actions. <br>
Risk: The workflow asks users to provide API secrets in chat and may display newly created API key secrets. <br>
Mitigation: Treat transcripts as sensitive, avoid sharing sessions that contain keys, and rotate any API secret exposed during use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vinhbui3004/aioz-stream-skill) <br>
- [AIOZ Stream API Base URL](https://api.aiozstream.network/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with curl command examples, tables, and response templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided AIOZ Stream public and secret keys during the session.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
