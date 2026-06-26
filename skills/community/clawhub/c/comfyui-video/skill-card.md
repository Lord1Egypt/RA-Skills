## Description: <br>
Automates AI video generation in ComfyUI with LTX-2.3 for text-to-video, image-to-video, batch scene rendering, troubleshooting, and performance tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a3165458](https://clawhub.ai/user/a3165458) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video creators use this skill to configure and operate ComfyUI LTX-2.3 workflows for T2V/I2V video generation, batch music-video scenes, progress checks, fault recovery, and performance tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The JavaScript helper changes the active ComfyUI graph and fetches a workflow from the local ComfyUI API. <br>
Mitigation: Review scripts/batch_scenes.js before use and run it only in the intended ComfyUI browser session. <br>
Risk: The workflow guidance includes SSH tunneling and remote output checks that could expose broader host access if run with excessive privileges. <br>
Mitigation: Use a least-privileged SSH account and limit access to the ComfyUI port and output paths required for generation. <br>
Risk: Untrusted model or workflow files can affect generated output and runtime behavior. <br>
Mitigation: Use trusted LTX-2.3 model, LoRA, VAE, and workflow files and verify paths before running batch generation. <br>


## Reference(s): <br>
- [ComfyUI Video skill page](https://clawhub.ai/a3165458/comfyui-video) <br>
- [Tips & Best Practices](references/tips.md) <br>
- [Workflow Node Reference](references/workflow_nodes.md) <br>
- [Batch scene automation script](scripts/batch_scenes.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ComfyUI workflow node IDs, model paths, SSH tunnel checks, batch scene configuration, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
