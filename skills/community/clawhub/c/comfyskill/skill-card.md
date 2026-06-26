## Description: <br>
Send prompts to a local ComfyUI instance to generate images based on user descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edward-hsiao](https://clawhub.ai/user/edward-hsiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to have an agent submit text-to-image prompts to a trusted ComfyUI endpoint and start image generation from a configured workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt and workflow data are sent to a ComfyUI endpoint. <br>
Mitigation: Use only a local or otherwise trusted COMFYUI_ENDPOINT. <br>
Risk: Generated images may be saved by ComfyUI according to the workflow. <br>
Mitigation: Review WORKFLOW_PATH and the ComfyUI workflow output settings before use. <br>
Risk: Network use is not formally permission-scoped. <br>
Mitigation: Install only when endpoint access is intended and review the configured endpoint before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edward-hsiao/comfyskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [Plain text status message after submitting a JSON workflow to ComfyUI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits prompt and workflow data to the endpoint configured by COMFYUI_ENDPOINT; generated images are saved by ComfyUI according to the workflow.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
