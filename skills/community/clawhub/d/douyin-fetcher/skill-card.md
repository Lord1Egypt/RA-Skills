## Description:

Douyin Fetcher helps an agent retrieve Douyin video files from Douyin links, including short videos and DASH-format long videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don068589](https://clawhub.ai/user/don068589)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to resolve Douyin links, extract video or audio stream URLs through browser inspection, and download or merge media files for later transcription, analysis, or storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser access, network requests, local downloads, and ffmpeg commands.

Mitigation: Run it with an isolated browser profile and approve each generated browser action, download command, and ffmpeg command before execution.

Risk: The skill writes media and transcript artifacts to local paths.

Mitigation: Use a user-approved output directory, limit file retention to the requested artifacts, and clean temporary media files after the workflow completes.

Risk: The security summary flags weak scoping and unsafe generated instructions.

Mitigation: Review or patch generated command and tool-call handling before allowing an agent to execute the workflow automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/don068589/skills/douyin-fetcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser tool-call examples, JavaScript snippets, shell commands, and local file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser-operation instructions, download commands, media file paths, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
