## Description: <br>
Run ComfyUI workflows from AI agents through a CLI that can import workflows, manage dependencies, execute across multiple ComfyUI servers, and track execution history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangyuchuh](https://clawhub.ai/user/huangyuchuh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn ComfyUI workflows into callable agent actions for image generation, workflow import, dependency checks, multi-server routing, and local workflow management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install ComfyUI custom nodes from third-party repositories. <br>
Mitigation: Review each repository before installation and install only dependencies from trusted sources. <br>
Risk: The local management UI and ComfyUI server controls can expose workflow and server operations if reachable from a network. <br>
Mitigation: Keep the Web UI and ComfyUI endpoints bound to localhost unless a separate access-control layer is in place. <br>
Risk: ComfyUI API keys or other server credentials may be used for cloud nodes. <br>
Mitigation: Avoid storing sensitive credentials unless required, restrict access to local configuration files, and rotate credentials after suspected exposure. <br>
Risk: Workflow imports, deletes, updates, and self-update behavior can alter local workflow and configuration data. <br>
Mitigation: Back up config and workflow data before bulk imports, deletes, or update operations. <br>
Risk: The skill may restart or force-stop local processes while managing the UI or updates. <br>
Mitigation: Run process-management actions only in a controlled local environment and review status output before retrying failed starts or updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huangyuchuh/comfyui-skill-openclaw) <br>
- [Workflow Import Reference](references/workflow-import.md) <br>
- [Architecture](docs/architecture.md) <br>
- [Use Cases](docs/use-cases.md) <br>
- [ComfyUI Native Local Routes](docs/comfyui-native-routes.md) <br>
- [ComfyUI server overview](https://docs.comfy.org/development/comfyui-server/comms_overview) <br>
- [ComfyUI server routes](https://docs.comfy.org/development/comfyui-server/comms_routes) <br>
- [ComfyUI Skill CLI](https://github.com/HuangYuChuh/ComfyUI_Skill_CLI) <br>
- [ComfyUI Skill CLI on PyPI](https://pypi.org/project/comfyui-skill-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON argument examples; runtime commands return JSON status data and generated file references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workflow IDs, prompt IDs, dependency reports, server status, and image output paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
