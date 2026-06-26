## Description: <br>
Generate images with Flux 2 Klein on RunComfy via the local RunComfy CLI, with model-specific guidance for choosing the 4B or 9B variant, setting image parameters, and writing effective prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent operators use this skill to generate image assets through RunComfy-hosted Flux 2 Klein, especially for fast concepting, product visualization, brand styling, and final 9B polish passes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunComfy account credentials or a RUNCOMFY_TOKEN value are required to execute generation requests. <br>
Mitigation: Use the RunComfy CLI login flow for local use or a scoped environment token in CI, and avoid storing tokens in shared project files. <br>
Risk: Prompts, reference image URLs, and generated-output requests are sent to RunComfy under the user's account. <br>
Mitigation: Submit only prompts and media that are appropriate for the user's approved RunComfy usage and data-handling requirements. <br>
Risk: Generated files may be downloaded into the output directory selected by the user. <br>
Mitigation: Choose an explicit output directory and review generated files before sharing them or using them downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/flux-2-klein) <br>
- [RunComfy](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein) <br>
- [Flux 2 Klein 9B model endpoint](https://www.runcomfy.com/models/blackforestlabs/flux-2-klein/9b/text-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein) <br>
- [Flux 2 Klein 4B model endpoint](https://www.runcomfy.com/models/blackforestlabs/flux-2-klein/4b/text-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein) <br>
- [RunComfy CLI introduction](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON CLI input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke RunComfy to produce result JSON and downloaded generated image files in a user-selected output directory.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
