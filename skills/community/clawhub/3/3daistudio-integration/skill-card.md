## Description: <br>
Convert images and text prompts to 3D models (.glb) using the 3D AI Studio API, with support for TRELLIS.2, Hunyuan Rapid, and Hunyuan Pro models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whale-professor](https://clawhub.ai/user/whale-professor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, artists, and automation agents use this skill to submit image or text inputs to 3D AI Studio, poll generation jobs, and save generated .glb models for downstream asset workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, and related metadata are sent to 3D AI Studio. <br>
Mitigation: Use only content approved for that provider and avoid sensitive, proprietary, regulated, or personal images unless permitted by the organization. <br>
Risk: Generated assets are downloaded from provider-supplied URLs without enough documented scoping. <br>
Mitigation: Validate generated asset URLs before fetching them and scan downloaded model files before using them in production workflows. <br>
Risk: Generation jobs consume third-party service credits. <br>
Mitigation: Confirm account balance and expected credit cost before submitting jobs, especially for Hunyuan Pro or textured outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whale-professor/3daistudio-integration) <br>
- [3D AI Studio homepage](https://www.3daistudio.com) <br>
- [3D AI Studio API platform](https://www.3daistudio.com/Platform/API) <br>
- [3D AI Studio API documentation](https://www.3daistudio.com/Platform/API/Documentation) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [CLI text plus generated .glb model files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires THREE_D_AI_STUDIO_API_KEY; generations consume provider credits and may block while polling.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
