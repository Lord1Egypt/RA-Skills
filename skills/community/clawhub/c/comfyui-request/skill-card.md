## Description: <br>
Send a workflow request to ComfyUI and return image results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Xtopher86](https://clawhub.ai/user/Xtopher86) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to submit ComfyUI workflows to a trusted ComfyUI server and receive JSON image results for agent-driven image generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends workflow content and optional Basic Auth credentials to the configured ComfyUI server over HTTP. <br>
Mitigation: Use only ComfyUI servers you control or trust, set COMFYUI_HOST and COMFYUI_PORT explicitly, avoid reused passwords, and prefer a trusted local network, VPN, or HTTPS reverse proxy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Xtopher86/comfyui-request) <br>
- [Publisher profile](https://clawhub.ai/user/Xtopher86) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, configuration] <br>
**Output Format:** [JSON object containing success status, prompt ID, image metadata, and image URLs; error responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses COMFYUI_HOST, COMFYUI_PORT, and optional COMFYUI_USER and COMFYUI_PASS configuration; supports timeout, polling interval, and first-image options.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
