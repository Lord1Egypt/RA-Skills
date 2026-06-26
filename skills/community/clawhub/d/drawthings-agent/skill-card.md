## Description: <br>
Generate images using Draw Things app via dt-skill CLI or MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mijuu](https://clawhub.ai/user/mijuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images through a local Draw Things setup, preferring the MCP generate_image tool when available and falling back to dt-skill CLI commands when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install an unpinned global npm package. <br>
Mitigation: Review the install before running it, and prefer pinning or approving a known @mijuu/drawthings package version. <br>
Risk: The skill may change local Draw Things configuration and start long-running image generation jobs. <br>
Mitigation: Confirm local model and server paths before configuration changes, and set timeouts appropriate for upscale-heavy jobs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local image-generation setup, model selection, prompt requirements, upscaling options, and timeout handling.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
