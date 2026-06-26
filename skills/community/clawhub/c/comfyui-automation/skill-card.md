## Description: <br>
Use when you need to automate ComfyUI tasks, including installing ComfyUI, parsing API-format workflow JSON files, checking and downloading missing models, and executing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nhuquangls](https://clawhub.ai/user/nhuquangls) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up ComfyUI, inspect API-format workflows for required model files, prepare missing model downloads, and submit workflows to a local ComfyUI API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to clone custom node repositories, install Python packages, and download model files into a ComfyUI workspace. <br>
Mitigation: Confirm each repository and model URL before execution, prefer trusted sources and pinned commits, and avoid automatic installation of unknown custom nodes. <br>
Risk: Workflow execution depends on locally available model files and a running ComfyUI server. <br>
Mitigation: Run the included model analysis script before execution, download only missing files without overwriting existing assets, and report missing nodes, missing models, or out-of-memory failures explicitly. <br>


## Reference(s): <br>
- [ComfyUI Repository](https://github.com/comfyanonymous/ComfyUI.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file checks, model download commands, ComfyUI custom node installation steps, and a lightweight Python API submission wrapper.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
