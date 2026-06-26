## Description: <br>
Checks the health status of a configured local ComfyUI instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xtopher86](https://clawhub.ai/user/Xtopher86) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ComfyUI users can use this skill to check whether a trusted local ComfyUI service is reachable at the configured host and port. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release notes and artifact prose describe run and stop actions, but the reviewed code only supports status checks. <br>
Mitigation: Use this version only to check ComfyUI reachability; do not rely on it to start or stop ComfyUI. <br>
Risk: The health check contacts a configurable host and port. <br>
Mitigation: Set COMFYUI_HOST and COMFYUI_PORT to a trusted ComfyUI instance, and avoid placing credentials in a .env file unless a later reviewed version uses them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xtopher86/comfyui-runner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON status response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports ok, status or error details, host, and port; non-status actions return only_status_supported_in_container.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
