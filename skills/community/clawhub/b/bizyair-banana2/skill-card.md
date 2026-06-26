## Description: <br>
Generates images with the BizyAir API and Nano Banana 2 model, including text-to-image, reference-image, and meme generation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin-chen2026](https://clawhub.ai/user/kevin-chen2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to call BizyAir cloud image generation from an agent workflow, producing image files from prompts and optional reference images without local GPU resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected reference images are sent to BizyAir for third-party processing. <br>
Mitigation: Avoid confidential or personal images unless the user accepts third-party processing. <br>
Risk: Successful image generations can incur pay-per-use charges. <br>
Mitigation: Keep the API key scoped and private, monitor spending, and invoke the skill explicitly for intended generations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevin-chen2026/bizyair-banana2) <br>
- [BizyAir website](https://www.bizyair.cn) <br>
- [BizyAir documentation](https://docs.bizyair.cn) <br>
- [BizyAir API reference](https://docs.bizyair.cn/api/api-reference.html) <br>
- [BizyAir pricing](https://docs.bizyair.cn/pricing/introduce.html) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, JSON, files] <br>
**Output Format:** [Markdown guidance with command examples; the bundled script writes image files and can print JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a BizyAir API key and may upload prompts and selected reference images to BizyAir.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
