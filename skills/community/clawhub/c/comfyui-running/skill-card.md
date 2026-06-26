## Description: <br>
全自动运行 ComfyUI 工作流：通过 REST API 执行工作流，支持 Windows / Linux / WSL 跨平台。By comfyui资源网 - www.comfyorg.cn <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentopen](https://clawhub.ai/user/agentopen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ComfyUI users use this skill to configure, start, and drive a local ComfyUI workflow from an agent, including prompt updates and retrieval of generated output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start and keep a local ComfyUI process running. <br>
Mitigation: Review the configured ComfyUI root and Python path before use, keep ComfyUI bound to localhost, and retain a manual stop procedure for the process. <br>
Risk: The skill may install Python packages while preparing runtime dependencies. <br>
Mitigation: Use a dedicated virtual environment and install pinned dependencies explicitly before enabling agent-driven execution. <br>
Risk: The skill can control a local Chrome or Edge debugging tab through CDP automation. <br>
Mitigation: Use an isolated browser profile and expose the debugging port only on localhost for the ComfyUI session. <br>
Risk: The skill can clear pending ComfyUI queue entries and save generated outputs to the configured output directory. <br>
Mitigation: Confirm queue state and output paths before execution, especially on shared ComfyUI installations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentopen/comfyui-running) <br>
- [comfyui资源网](https://www.comfyorg.cn) <br>
- [comfyui资源网 tutorials](https://www.comfyorg.cn/tutorial) <br>
- [comfyui资源网 workflows](https://www.comfyorg.cn/workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Agent-facing text, Python snippets, shell commands, JSON configuration, and generated image file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the user's local ComfyUI installation, workflow files, configured output directory, and localhost ComfyUI service.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
