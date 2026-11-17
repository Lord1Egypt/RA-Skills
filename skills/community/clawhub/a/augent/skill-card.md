## Description:

The audio & video layer for agents. 22 local MCP tools. No cloud, no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[augentdevs](https://clawhub.ai/user/augentdevs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Augent to give an agent local audio and video capabilities, including media download, transcription, search, note generation, clipping, speaker identification, visual frame extraction, and text-to-speech.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an external package and depends on local media-processing binaries.

Mitigation: Pin or verify the augent package version where possible, and install ffmpeg, yt-dlp, and aria2c from trusted package sources before enabling the MCP server.

Risk: The skill stores searchable transcripts and writes media outputs to local folders.

Mitigation: Use the AUGENT_DOWNLOAD_DIR, AUGENT_NOTES_DIR, and AUGENT_MEMORY_DIR settings to keep outputs in intended locations, and clear memory only when local data removal is intended.

Risk: X/Twitter Spaces recording may use a user-created local auth file.

Mitigation: Provide the auth file only when Spaces recording is needed, and protect it as a local credential.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/augentdevs/skills/augent)
- [Augent Documentation](https://docs.augent.app)
- [Augent Website](https://augent.app)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Text, Markdown notes, timestamped transcript/search results, generated media files, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write downloads, notes, clips, text-to-speech output, visual frames, and persistent transcription memory to local paths configured by the user.]

## Skill Version(s):

1.5.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
