## Description: <br>
Discovers podcast topics, supports research and script generation with citations, prepares text for ElevenLabs TTS, and stores generated podcast assets locally or in S3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harshilmathur](https://clawhub.ai/user/harshilmathur) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and automation workers use this skill to discover podcast topics from configured sources, generate researched scripts with citations, prepare narration text, and persist podcast outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automatic workflow may proceed toward audio generation or storage before users have reviewed intermediate outputs. <br>
Mitigation: Run manual mode first and inspect generated scripts and verification reports before audio generation or upload. <br>
Risk: Podcast content may be sent to configured providers or persisted in S3/local storage. <br>
Mitigation: Avoid sensitive unpublished content unless the configured providers are trusted, and use dedicated least-privilege AWS/S3 and ElevenLabs credentials. <br>
Risk: Cron scheduling or public S3 configuration can create recurring production behavior or remote public persistence. <br>
Mitigation: Do not enable cron or public S3 access unless recurring production and remote/public persistence are intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harshilmathur/custom-podcast-discovery) <br>
- [Publisher Profile](https://clawhub.ai/user/harshilmathur) <br>
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Audio, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; generated pipeline artifacts include JSON, text, verification reports, TTS-ready text, and MP3 audio.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be written to local storage or uploaded to user-configured S3 storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
