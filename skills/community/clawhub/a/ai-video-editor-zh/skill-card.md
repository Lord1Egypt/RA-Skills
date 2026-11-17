## Description:

AI 视频剪辑器 helps an agent submit MP4 videos to Sparki for AI-assisted editing, captions, commentary, aspect-ratio changes, highlights, vlogs, montages, and short-form clips, then return a time-limited download link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route video-editing requests through Sparki, including long-to-short conversion, highlight generation, subtitles, commentary, and platform-specific aspect ratios. It is intended for workflows where uploading the source video to the Sparki/aicoding.live service is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local videos to a cloud service.

Mitigation: Use it only for videos that are acceptable to share with the Sparki/aicoding.live service.

Risk: The security review flags unsafe API-key handling guidance, including a documented key-status command.

Mitigation: Use a dedicated low-privilege SPARKI_API_KEY from a managed secret store, avoid the key-status command, and do not persist secrets in shell profiles or .env files.

Risk: The install command and API endpoint affect where videos and credentials are sent.

Mitigation: Verify the ClawHub install target and Sparki/aicoding.live API endpoint before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/ai-video-editor-zh)
- [Publisher profile](https://clawhub.ai/user/fischerlam)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and plain-text result identifiers or download URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads local MP4 files up to 3 GB, polls asynchronous processing, and returns a result URL documented as valid for 24 hours.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
