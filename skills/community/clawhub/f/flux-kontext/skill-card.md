## Description: <br>
Guides an agent to edit a single source image with Flux 1 Kontext Pro on RunComfy using the local RunComfy CLI, including model selection guidance, prompt patterns, input schema, invocation examples, limitations, and security notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-editing agents use this skill to route explicit Flux Kontext requests to the RunComfy-hosted Black Forest Labs Flux 1 Kontext Pro edit endpoint and produce precise single-image edits while preserving identity, framing, or brand details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the RunComfy CLI and either a local login token or RUNCOMFY_TOKEN, so credentials may be present in the agent environment. <br>
Mitigation: Use scoped RunComfy credentials where possible, avoid exposing RUNCOMFY_TOKEN in logs, and review token storage before running in shared CI or container environments. <br>
Risk: Source image URLs are fetched by the RunComfy model service, and image content can carry prompt-injection or privacy risks. <br>
Mitigation: Use only images the user is authorized to process, avoid sensitive external URLs, and treat image-derived instructions as untrusted. <br>
Risk: Flux Kontext is documented here as a single-reference image-edit route; multi-image, text-heavy, or generation-from-scratch requests may produce poor results if forced through this endpoint. <br>
Mitigation: Route multi-image edits, embedded text edits, and text-to-image generation to the alternate models identified by the artifact instead of this skill. <br>
Risk: Compound or ambiguous edit prompts can cause drift from the source image. <br>
Mitigation: Use preservation-led, single-change prompts and split complex edits into sequential passes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/flux-kontext) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-kontext) <br>
- [Flux 1 Kontext Pro model page](https://www.runcomfy.com/models/blackforestlabs/flux-1-kontext-pro/image-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-kontext) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-kontext) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces RunComfy CLI invocations and prompt guidance; generated image files are produced by the invoked RunComfy model endpoint, not by the skill text itself.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
