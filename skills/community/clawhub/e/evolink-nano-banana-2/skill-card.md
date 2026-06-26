## Description: <br>
Nano Banana 2 - AI image generation powered by Google Gemini 3.1 Flash, supporting fast text-to-image and image editing through the Evolink API with one API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and external users use this skill to guide an agent through Nano Banana 2 image generation or editing workflows, including prompt collection, optional image upload, asynchronous generation, polling, and result handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, and generated outputs are sent to Evolink for external processing. <br>
Mitigation: Use the skill only for content you intend to process through Evolink, and avoid confidential, regulated, or proprietary images unless that external processing is acceptable. <br>
Risk: Uploaded files and generated result URLs are temporary shareable links. <br>
Mitigation: Treat links as shareable while they exist, save needed outputs promptly, and delete hosted files when they are no longer needed. <br>
Risk: Using the optional MCP package with @latest can pull future package changes automatically. <br>
Mitigation: Pin @evolinkai/evolink-media to a reviewed version in production or controlled environments. <br>


## Reference(s): <br>
- [Nano Banana 2 Skill Page](https://clawhub.ai/EvoLinkAI/evolink-nano-banana-2) <br>
- [Evolink](https://evolink.ai) <br>
- [Evolink Media MCP Server](https://github.com/EvoLinkAI/evolink-media-mcp) <br>
- [@evolinkai/evolink-media npm Package](https://www.npmjs.com/package/@evolinkai/evolink-media) <br>
- [Nano Banana 2 Image API Parameter Reference](references/image-api-params.md) <br>
- [Evolink File Hosting API - Image Upload](references/file-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API parameters, MCP setup commands, status updates, and result URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOLINK_API_KEY; image generation is asynchronous and result URLs expire after 24 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
