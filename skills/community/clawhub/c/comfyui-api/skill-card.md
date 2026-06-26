## Description: <br>
Connects to a ComfyUI server to generate images from prompts, auto-detects URLs, translates Chinese prompts, and supports REST and WebSocket APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqliaoxin](https://clawhub.ai/user/qqliaoxin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to connect an agent to a ComfyUI server, set the server URL, check status, and generate images from text prompts through REST or WebSocket APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files to the configured ComfyUI server. <br>
Mitigation: Use only a ComfyUI server you control or trust, confirm the configured URL before generation, and avoid running upload actions on sensitive local files. <br>
Risk: The skill can inspect queue/history information and cancel or interrupt work on the configured server. <br>
Mitigation: Use it only with servers where you are authorized to manage running jobs, and review status or control actions before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqliaoxin/comfyui-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration instructions] <br>
**Output Format:** [Markdown and structured status/result text with image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connects to a configured ComfyUI server; generation results depend on that server's models, queue, and API availability.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
