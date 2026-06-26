## Description: <br>
ComfyUI Painter controls a local ComfyUI image-generation workflow, integrates CivitAI model search, downloads, update checks, and parameter tuning, and can send generated images to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeron-G](https://clawhub.ai/user/zeron-G) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and image-generation users use this skill to run local ComfyUI text-to-image and image-to-video workflows, manage CivitAI checkpoints, tune generation settings, and share generated outputs through Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a local ComfyUI instance and may expose it beyond the local machine if remote binding is enabled. <br>
Mitigation: Restrict activation to explicit image-generation commands and bind ComfyUI to localhost unless remote access is intentional. <br>
Risk: The skill can download third-party model files and write local configuration. <br>
Mitigation: Require confirmation before downloads or persistent config changes, and reject absolute paths or path separators in requested filenames. <br>
Risk: The shutdown helper can terminate Python processes too broadly. <br>
Mitigation: Use PID-specific shutdown for the ComfyUI process instead of a blanket Python process kill command. <br>
Risk: Generated images may be sent to Discord and the skill uses a CivitAI API key. <br>
Mitigation: Confirm intended sharing destinations before posting outputs and keep API credentials scoped and protected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zeron-G/comfyui-painter) <br>
- [CivitAI API](https://civitai.com/api/v1) <br>
- [Local design notes](artifact/DESIGN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON-like result objects from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local API calls, file writes, model downloads, ComfyUI process management, and Discord image sharing when executed by an agent.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
