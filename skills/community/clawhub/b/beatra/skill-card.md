## Description:

Beatra Universal helps an agent create and manage AI images, videos, music, and speech, and retrieve public social data across YouTube, TikTok, Instagram, and X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and social media researchers use the skill to produce and manage AI-generated images, video, music, and speech, or to retrieve public social data for research and planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious, citing automatic installation-linked telemetry and privacy gaps for user media and text sent to the service; scanner coverage is partial.

Mitigation: Review telemetry and data-transfer practices, and send only content intended for the service.

Risk: ClawScan reports a possible uninstall safety issue.

Mitigation: Review the uninstall behavior and confirm the files and shared connection affected before running it.

Risk: Security guidance notes that updates run an unpinned CLI.

Mitigation: Review update changes before applying them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/beatra)
- [Beatra package information](https://beatra.ai/install)
- [Image workflows](artifact/references/images.md)
- [Video workflows](artifact/references/videos.md)
- [Music and speech workflows](artifact/references/speech-and-audio.md)
- [Public social data](artifact/references/social.md)
- [Updates and security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Images, Video, Audio, Music, Text, JSON, Files]

**Output Format:** [Generated media files, transcripts and subtitles, prompts or scripts, and public social data in JSON; media formats vary by model.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reports the actual format and dimensions of returned media. Some creative operations may use account credits.]

## Skill Version(s):

3.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
