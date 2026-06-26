## Description: <br>
Audio/video information extraction, format conversion, and audio extraction using FFmpeg WASM sandbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect media files, convert video formats, and extract audio through an FFmpeg WebAssembly component executed by the OpenClaw WASM sandbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs a remote WASM executable without pinned integrity verification. <br>
Mitigation: Install only when the openclaw-wasm-sandbox plugin and WASM binary are trusted, and independently verify a pinned release and checksum before processing explicit media files. <br>


## Reference(s): <br>
- [Boxed FFmpeg on ClawHub](https://clawhub.ai/guyoung/boxed-ffmpeg) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell and JavaScript tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires openclaw-wasm-sandbox >= 0.2.0 and a local boxed-ffmpeg WASM file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
