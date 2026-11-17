## Description:

FFmpeg operations via the ffmpeg-static npm package (bundled binary) with automatic fallback to a native system FFmpeg installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantox](https://clawhub.ai/user/fantox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and generate FFmpeg commands, Node.js integration snippets, and configuration guidance for transcoding, stream manipulation, thumbnail extraction, format conversion, and FFmpeg binary resolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an npm package that installs an executable FFmpeg binary.

Mitigation: Pin exact package versions, use a lockfile or checksum verification, and install only from a trusted package source.

Risk: Several command templates overwrite outputs by default with `-y`.

Mitigation: Use unique output paths or explicit overwrite checks when preserving existing files matters.

Risk: FFmpeg can read URLs and protocol inputs, so untrusted filenames or URLs can expand the scope of what a command accesses.

Mitigation: Validate media paths and URLs before execution and run jobs in a low-privilege workspace.

## Reference(s):

- [FFmpeg Static API Reference](artifact/references/api_reference.md)
- [ffmpeg-static GitHub repository](https://github.com/eugeneware/ffmpeg-static)
- [ffmpeg-static npm package](https://www.npmjs.com/package/ffmpeg-static)
- [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html)
- [ClawHub skill page](https://clawhub.ai/fantox/skills/ffmpeg-static)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npm; outputs should account for FFMPEG_PATH overrides, system FFmpeg fallback, and bundled ffmpeg-static behavior.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
