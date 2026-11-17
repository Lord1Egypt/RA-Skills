## Description:

Automates ComfyUI setup, API-format workflow analysis, missing-model checks, model download guidance, and local workflow execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhuquangls](https://clawhub.ai/user/nhuquangls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up ComfyUI, prepare API-format workflows, check model dependencies, and queue image-generation jobs through a local ComfyUI API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead agents to install unpinned third-party code or ComfyUI custom nodes.

Mitigation: Use an isolated workspace or container, pin ComfyUI and each custom node to reviewed commits, and require manual approval before adding new custom-node repositories.

Risk: Model downloads may lack clear provenance or integrity checks.

Mitigation: Verify model sources and checksums before downloading or using large model files.

## Reference(s):

- [ComfyUI GitHub Repository](https://github.com/comfyanonymous/ComfyUI)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup steps, model dependency reports, download commands, workflow API wrappers, and error-reporting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
