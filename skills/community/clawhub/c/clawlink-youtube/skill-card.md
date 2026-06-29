## Description: <br>
Manage YouTube channels, videos, comments, playlists, and creator workflows via the YouTube Data API v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to inspect YouTube channel data, manage video metadata, moderate comments, work with playlists and subscriptions, and retrieve creator insights through a connected ClawLink YouTube account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting a YouTube/Google account through ClawLink OAuth. <br>
Mitigation: Install only when that account connection is intended, and review the OAuth permissions shown during the connection flow. <br>
Risk: Write operations can change or delete YouTube videos, playlists, subscriptions, or comments. <br>
Mitigation: Require a clear preview and explicit user confirmation before any create, update, or delete action. <br>
Risk: The available YouTube tools are dynamic and may differ from examples in the skill text. <br>
Mitigation: List or search the live ClawLink YouTube tool catalog before selecting a tool, and describe unfamiliar tools before calling them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/clawlink-youtube) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=clawlink-youtube) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [YouTube Data API v3](https://developers.google.com/youtube/v3) <br>
- [YouTube API Reference](https://developers.google.com/youtube/v3/docs) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON parameter snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live ClawLink YouTube tool catalog as the source of truth for available actions.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
