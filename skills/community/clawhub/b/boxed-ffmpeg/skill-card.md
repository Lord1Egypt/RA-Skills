## Description:

Audio/video information extraction, format conversion, and audio extraction using FFmpeg WASM sandbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media workflow operators use this skill to inspect audio/video files, convert video formats, and extract audio through a local FFmpeg WebAssembly sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unverified WASM binary downloaded from a mutable GitHub URL.

Mitigation: Use a packaged or pinned WASM artifact with a published SHA-256 or signature before running media jobs.

Risk: The skill asks users to install or update the openclaw-wasm-sandbox gateway plugin.

Mitigation: Install or update the plugin only from a trusted source and review the plugin before enabling it.

Risk: Media processing writes outputs into the selected working directory.

Mitigation: Run jobs in a dedicated directory containing only the intended input and output files.

## Reference(s):

- [Boxed FFmpeg ClawHub listing](https://clawhub.ai/guyoung/skills/boxed-ffmpeg)
- [Boxed FFmpeg WASM component](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-ffmpeg/files/boxed-ffmpeg-component.wasm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and JavaScript command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local media jobs in the selected workDir and write output files there.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
