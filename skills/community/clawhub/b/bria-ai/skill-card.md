## Description: <br>
Bria.ai image API skill for generating images from text prompts, editing images with natural language, removing backgrounds for transparent PNGs, and creating product lifestyle shots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galbria](https://clawhub.ai/user/galbria) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to connect to Bria.ai services for image generation, background removal, image editing, upscaling, and product photography workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Bria access credentials under ~/.bria/credentials. <br>
Mitigation: Restrict local file permissions for cached credentials and delete ~/.bria/credentials when cached access is no longer needed. <br>
Risk: Selected images, image URLs, and prompts are sent to Bria's external service for processing. <br>
Mitigation: Use the skill only with content that is permitted by the user's data policy, especially for confidential or sensitive images. <br>
Risk: API access depends on a valid Bria account, token state, billing status, and quota. <br>
Mitigation: Verify authentication and billing status before API calls, and stop when the skill reports billing or token errors. <br>


## Reference(s): <br>
- [Bria homepage](https://bria.ai) <br>
- [Bria API docs for agents](https://docs.bria.ai/llms.txt) <br>
- [Capabilities and prompt recipes](references/capabilities.md) <br>
- [API endpoints reference](references/api-endpoints.md) <br>
- [ClawHub skill page](https://clawhub.ai/galbria/skills/bria-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash snippets, configuration steps, and Bria API result URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bria credentials or a BRIA_API_KEY; generated or edited image outputs may be returned as Bria-hosted URLs.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
