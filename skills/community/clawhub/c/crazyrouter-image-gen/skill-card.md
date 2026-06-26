## Description: <br>
Generates images from text prompts through the Crazyrouter API with model, size, count, and quality options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users can use this skill to generate image files from prompts through Crazyrouter-supported image models. It is useful when an agent needs to create, save, and report generated image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and related request metadata are sent to Crazyrouter and may be routed to underlying model providers. <br>
Mitigation: Avoid secrets, confidential project details, regulated data, or private personal information unless Crazyrouter's data handling terms have been reviewed and approved. <br>
Risk: The skill requires a Crazyrouter API key and makes third-party network requests during image generation. <br>
Mitigation: Provide CRAZYROUTER_API_KEY only in trusted environments and confirm the requested output path before running the generation command. <br>


## Reference(s): <br>
- [Crazyrouter](https://crazyrouter.com) <br>
- [ClawHub skill page](https://clawhub.ai/xujfcn/crazyrouter-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Image files plus concise terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRAZYROUTER_API_KEY and writes one or more image files to the requested output path.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
