## Description:

全自动运行 ComfyUI 工作流：通过 REST API 执行工作流，支持 Windows / Linux / WSL 跨平台。By comfyui资源网 - www.comfyorg.cn

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentopen](https://clawhub.ai/user/agentopen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ComfyUI users use this skill to let an agent configure, start, and operate a local ComfyUI workflow for image generation across Windows, Linux, macOS, or WSL environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start ComfyUI, install missing Python packages, and control a Chrome or Edge debugging session on the local machine.

Mitigation: Review the configured ComfyUI, Python, and browser paths before use, and run the skill in an isolated environment when possible.

Risk: The skill starts ComfyUI with broad network binding and interacts with local ComfyUI REST endpoints.

Mitigation: Change ComfyUI startup to bind to 127.0.0.1 unless wider network access is explicitly required.

Risk: The skill can write generated images to the ComfyUI output folder and may clear pending ComfyUI jobs.

Mitigation: Avoid sharing the same ComfyUI queue with other users and verify that pending jobs belong to the intended session before running automation.

Risk: Browser debugging automation may attach to an unintended tab if the local debugging session is reused.

Mitigation: Confirm the debugging tab is the intended ComfyUI page before allowing the skill to control it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentopen/skills/comfyui-running)
- [comfyui资源网](https://www.comfyorg.cn)
- [ComfyUI tutorials](https://www.comfyorg.cn/tutorial)
- [ComfyUI workflows](https://www.comfyorg.cn/workflow)
- [ComfyUI package resource](https://www.comfyorg.cn/shop/1680.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, JSON configuration, and ComfyUI output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May queue ComfyUI workflows and return status, prompt IDs, and generated image paths from the configured ComfyUI output directory.]

## Skill Version(s):

3.0.2 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
