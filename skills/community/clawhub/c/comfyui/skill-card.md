## Description:

Run local ComfyUI workflows via the HTTP API. Use when the user asks to run ComfyUI, execute a workflow by file path/name, or supply raw API-format JSON; supports the default workflow bundled in assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelvincai522](https://clawhub.ai/user/kelvincai522)

### License/Terms of Use:


## Use Case:

Developers and image-generation users use this skill to edit and run local ComfyUI workflow JSON, queue workflows through the ComfyUI HTTP API, and locate generated image outputs. It also helps place model weight files under a local ComfyUI installation when users provide model URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install or run external software in a local ComfyUI setup.

Mitigation: Review the skill before installation, use only trusted ComfyUI environments, and pin or verify ComfyUI dependencies where possible.

Risk: Model weight downloads can come from arbitrary user-provided URLs.

Mitigation: Use only trusted model URLs, verify downloaded files when possible, and avoid pasted URL lists from untrusted sources.

Risk: The downloader may install pget automatically if it is missing.

Mitigation: Prefer --no-pget unless pget is already installed from a trusted source.

Risk: Custom workflow JSON can affect local ComfyUI execution behavior.

Mitigation: Inspect workflow JSON before running it and avoid workflows from untrusted sources.

## Reference(s):

- [ComfyUI Skill on ClawHub](https://clawhub.ai/kelvincai522/skills/comfyui)
- [ComfyUI upstream project](https://github.com/comfyanonymous/ComfyUI.git)
- [pget downloader](https://github.com/replicate/pget)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local workflow JSON edits, ComfyUI API run results, model download paths, and generated image file paths.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
