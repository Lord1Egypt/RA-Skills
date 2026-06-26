## Description: <br>
Comfyui helps an agent run local ComfyUI image-generation workflows for text-to-image, image-to-image, and ControlNet tasks with automatic server management, WebSocket progress tracking, and optional Feishu image sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjy520crl](https://clawhub.ai/user/wjy520crl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate or transform images through a local ComfyUI desktop/server setup, including conversational prompts and command-line workflows. It is intended for local image generation with optional delivery of generated images to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local service control may stop broader processes than intended. <br>
Mitigation: Review and narrow the stop/restart commands before use, especially any path that can terminate all python.exe processes. <br>
Risk: Generated images may be uploaded or sent through Feishu with low visibility. <br>
Mitigation: Require explicit user confirmation and destination review before enabling Feishu upload or send behavior. <br>
Risk: Model weights or helper executables may be downloaded from external sources. <br>
Mitigation: Verify download sources, hashes, and executable provenance before running downloaded helpers or model assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjy520crl/comfyui-pro) <br>
- [Publisher profile](https://clawhub.ai/user/wjy520crl) <br>
- [README](artifact/README.md) <br>
- [pget project](https://github.com/replicate/pget) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Generated local image files with concise status or error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated images locally and optionally upload or send them through Feishu when configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
