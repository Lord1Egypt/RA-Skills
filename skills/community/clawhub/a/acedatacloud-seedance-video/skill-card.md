## Description: <br>
Generate AI dance and motion videos with Seedance (ByteDance) via AceDataCloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Germey](https://clawhub.ai/user/Germey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-creation teams use this skill to generate short motion videos from text prompts or animate a single image through the AceDataCloud Seedance API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and request metadata are sent to AceDataCloud and downstream video-generation providers. <br>
Mitigation: Do not submit secrets, confidential business content, private personal images, or regulated data unless approved and covered by provider privacy, retention, and billing terms. <br>
Risk: Generated video requests can fail when unsupported durations or incompatible image-to-video inputs are used. <br>
Mitigation: Keep duration values within the documented 2-12 second range and provide a single image URL for image-to-video workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Germey/acedatacloud-seedance-video) <br>
- [AceDataCloud Seedance video API endpoint](https://api.acedata.cloud/seedance/videos) <br>
- [Hosted Seedance MCP endpoint](https://seedance.mcp.acedata.cloud/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash, JSON, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers authentication, model selection, text-to-video and image-to-video request payloads, and task polling status handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
