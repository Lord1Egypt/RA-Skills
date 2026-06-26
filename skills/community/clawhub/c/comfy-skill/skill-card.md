## Description: <br>
Send user prompts to a local ComfyUI endpoint using the included workflow.json to generate images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edward-hsiao](https://clawhub.ai/user/edward-hsiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn text prompts into locally generated images through a ComfyUI workflow. It is intended for environments where the user controls or trusts the local ComfyUI service and selected image model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local ComfyUI endpoint and workflow, so execution can affect local files or development environments. <br>
Mitigation: Install only if the publisher is trusted, review the workflow before use, and run it against a ComfyUI instance and model configuration you control. <br>
Risk: Generated images depend on the configured model, prompt, and workflow behavior. <br>
Mitigation: Review generated outputs before publication or downstream use and apply the user's normal content and safety checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edward-hsiao/comfy-skill) <br>
- [Publisher profile](https://clawhub.ai/user/edward-hsiao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with command-style invocation and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local ComfyUI endpoint and the bundled workflow.json; generated image files are produced by ComfyUI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
