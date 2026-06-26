## Description: <br>
ComfyUI执行器 connects an agent to a ComfyUI server over HTTP to run image, video, or audio workflows, upload files, inspect capabilities, and manage queues and memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chsengni](https://clawhub.ai/user/chsengni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate ComfyUI workflows, upload workflow inputs, inspect available models and nodes, retrieve generated outputs, and manage service queues or memory during local or trusted-server generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete workflow files, interrupt running jobs, clear ComfyUI history, and request memory-management operations. <br>
Mitigation: Review commands before execution and require explicit user confirmation before delete, interrupt, clear-history, free-memory, or unload-model actions. <br>
Risk: Downloaded output filenames and output directories may be influenced by the ComfyUI server response or runtime arguments. <br>
Mitigation: Use only trusted ComfyUI servers, constrain output directories to expected locations, and validate downloaded filenames before writing files. <br>
Risk: The skill can connect to configurable ComfyUI server URLs and optionally use API keys. <br>
Mitigation: Avoid untrusted servers, avoid sensitive API keys unless required, and keep API keys out of committed configuration files and public logs. <br>


## Reference(s): <br>
- [ComfyUI API Specification](references/api-specification.md) <br>
- [ComfyUI Workflow Format](references/workflow-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands, JSON workflow guidance, configuration notes, and file paths for generated outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference local output files downloaded from ComfyUI, including images, video, audio, model files, or other generated artifacts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
