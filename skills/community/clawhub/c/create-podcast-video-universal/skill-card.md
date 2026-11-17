## Description:

CreateVideo helps agents turn user-provided audio or text scripts into vertical videos with background media, optional ListenHub text-to-speech, ffmpeg merging, and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyken](https://clawhub.ai/user/jackyken)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, content operators, and developers can use this skill to generate short vertical videos from narration audio or a written script. It guides task folder creation, optional ListenHub TTS setup, ffmpeg-based media merging, and short promotional content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs and runs an unversioned third-party ListenHub MCP server from npm.

Mitigation: Pin and verify the MCP server package version before use, or run it in a restricted environment with minimal file, environment-variable, and network access.

Risk: Text sent for TTS may contain confidential or sensitive content.

Mitigation: Avoid sending confidential text to the TTS flow unless the user trusts the MCP server and the service handling the content.

Risk: Video generation depends on local ffmpeg and user-provided media assets.

Mitigation: Confirm ffmpeg and ffprobe are installed, review background video licensing, and verify template compatibility before producing final video files.

## Reference(s):

- [ListenHub MCP Reference](references/listenhub-guide.md)
- [ClawHub skill page](https://clawhub.ai/jackyken/skills/create-podcast-video-universal)
- [Publisher profile](https://clawhub.ai/user/jackyken)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands, configuration steps, file paths, and expected output notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an agent workflow for creating task directories, merging audio and video assets, and reporting generated video outputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
