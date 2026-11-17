## Description:

Generate images, faceswap, edit photos, animate expressions, and do style transfer via a self-hosted ComfyUI instance on your LAN.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bortlesboat](https://clawhub.ai/user/bortlesboat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route image generation, image editing, faceswap, expression animation, and style-transfer requests to their own LAN-hosted ComfyUI setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive, private, or face images may be sent to the configured bridge and may be queued on disk.

Mitigation: Use a trusted local or authenticated bridge, avoid plaintext non-loopback HTTP for private or face images, and clear queued image copies when they are no longer needed.

Risk: Queued background delivery can send generated images through iMessage to an unintended recipient.

Mitigation: Disable or tightly control the queue daemon and verify the intended iMessage recipient or chat target before enabling delivery.

Risk: The security evidence flags command-execution risk in the queue processor shell fallback and queue path handling.

Mitigation: Do not run the queue processor until the shell fallback and queue path validation issues are fixed, and do not process queue files from untrusted sources.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bortlesboat/skills/comfyui-bridge)
- [ComfyUI Bridge project homepage](https://github.com/Bortlesboat/comfyui-bridge)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Ollama](https://ollama.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs commonly include a MEDIA path to a generated image file; queued requests may later deliver results through the configured local workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
