## Description: <br>
Generate images using Black Forest Labs FLUX.2-pro via Azure AI Foundry with configurable dimensions, seeds, and optional Chinese text overlay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwcih](https://clawhub.ai/user/zwcih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate PNG images from text prompts through a configured Azure AI Foundry FLUX.2-pro endpoint. It also provides guidance for direct API calls, reproducible seeds, common dimensions, and CJK text overlay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured endpoint or overly broad API key could send prompts to the wrong Azure resource or expose unnecessary access. <br>
Mitigation: Use a scoped FLUX_API_KEY and confirm FLUX_ENDPOINT points to the intended Azure resource before running generation. <br>
Risk: Prompts may contain sensitive information that is sent to the configured image service. <br>
Mitigation: Avoid including confidential, personal, or regulated information in prompts. <br>
Risk: Optional Canvas dependencies and font files add supply-chain risk when installed from untrusted sources. <br>
Mitigation: Install Canvas and CJK font files only from trusted package and font sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zwcih/azure-flux-image-gen) <br>
- [Azure AI Foundry FLUX API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell and JavaScript examples; script output is a PNG image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLUX_ENDPOINT and FLUX_API_KEY; image generation is serialized with a 180 second timeout.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
