## Description:

Comfyui helps agents generate local images with ComfyUI using text-to-image, image-to-image, and ControlNet workflows, with server management, WebSocket progress, Feishu delivery, and GPU monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjy520crl](https://clawhub.ai/user/wjy520crl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-generation users use this skill to ask an agent for local ComfyUI image generation, including text-to-image, image-to-image, and ControlNet workflows. It can manage the local ComfyUI service, report generation progress, save image files, and optionally send results through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a local ComfyUI server and stop related processes.

Mitigation: Run it in a dedicated local environment and review the server start/stop commands before installing it on a workstation with other active Python or ComfyUI jobs.

Risk: The skill writes generated images to disk and can use Feishu credentials for image delivery.

Mitigation: Configure output paths and Feishu credentials with least privilege, and remove or disable Feishu delivery if it is not required.

Risk: The skill can download and run the pget helper executable for model downloads.

Mitigation: Review the download path before use, verify downloaded binaries and model sources, or use the no-pget path where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjy520crl/skills/comfyui-pro)
- [Publisher profile](https://clawhub.ai/user/wjy520crl)
- [pget GitHub project](https://github.com/replicate/pget)

## Skill Output:

**Output Type(s):** [Files, Text, API Calls, Shell commands, Configuration]

**Output Format:** [Generated image files with progress/status text and local service commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated images to disk and can send image results through Feishu when configured.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
