## Description:

Start the Clawface 3D avatar web UI - serves a local web page the user opens in their browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmfisher](https://clawhub.ai/user/nmfisher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to start a local Clawface avatar chat UI, connect it to the OpenClaw gateway, and return a browser URL for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local server can use OpenClaw credentials with broad authority.

Mitigation: Run only on a trusted machine and private network, use the least-privileged gateway token possible, and stop the node process when finished.

Risk: The web UI is intended for local use and exposes a gateway proxy.

Mitigation: Prefer loopback-only access and avoid exposing the service beyond the local host.

Risk: The skill installs and executes a native TTS runtime from downloaded artifacts.

Mitigation: Verify or pin the downloaded runtime and model artifacts before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nmfisher/skills/clawface)
- [sherpa-onnx runtime release for macOS](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-osx-universal2-shared.tar.bz2)
- [sherpa-onnx runtime release for Linux x64](https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2)
- [Piper en_US lessac high voice model](https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-lessac-high.tar.bz2)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and a local URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local Node.js server and returns the avatar UI URL.]

## Skill Version(s):

0.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
