## Description: <br>
Start the Clawface 3D avatar web UI - serves a local web page the user opens in their browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmfisher](https://clawhub.ai/user/nmfisher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to start a local Clawface 3D avatar chat interface with built-in TTS and a browser-accessible localhost URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local avatar web UI exposes broad credential-backed OpenClaw gateway access while the server is running. <br>
Mitigation: Use this only with trusted publishers and on a trusted browser and network; prefer a restricted token or dedicated identity when available. <br>
Risk: The running local server keeps gateway access available until the Node process is stopped. <br>
Mitigation: Stop the Node process when the avatar session is finished. <br>


## Reference(s): <br>
- [Clawface on ClawHub](https://clawhub.ai/nmfisher/clawface) <br>
- [sherpa-onnx runtime for macOS](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2) <br>
- [sherpa-onnx runtime for Linux x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2) <br>
- [Piper en_US lessac high voice model](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and a localhost URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js on macOS or Linux and downloaded sherpa-onnx runtime/model assets.] <br>

## Skill Version(s): <br>
0.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
