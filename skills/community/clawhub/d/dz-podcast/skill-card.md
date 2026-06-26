## Description: <br>
Generate and publish a dual-host daily podcast. Fetches news, generates a conversational script between two hosts, synthesizes audio via Fish Audio or Edge TTS, publishes to S3 with RSS feed for Apple Podcasts, Spotify, etc. Fully automated with cron support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dz1922](https://clawhub.ai/user/dz1922) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, podcast operators, and developers use this skill to assemble a daily news podcast workflow that turns fetched topics into a two-host script, synthesized audio, hosted MP3 episodes, and an RSS feed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated podcast content can be published automatically to public feeds and messaging channels. <br>
Mitigation: Review generated briefs, scripts, and audio before publishing, and test the workflow manually before enabling cron. <br>
Risk: The workflow depends on Fish Audio and AWS/S3 credentials. <br>
Mitigation: Use dedicated least-privilege credentials, keep API keys out of source files and logs, and publish to a non-sensitive bucket. <br>
Risk: Scripts and audio may be sent to external TTS, hosting, RSS, or messaging services. <br>
Mitigation: Use the skill only with content that is acceptable to share with the configured third-party services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dz1922/dz-podcast) <br>
- [RSS Feed Format Reference](references/rss-format.md) <br>
- [Fish Audio](https://fish.audio) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated text, audio, and RSS artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce publishable MP3 episodes and RSS feed updates when configured with external TTS and S3 credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
