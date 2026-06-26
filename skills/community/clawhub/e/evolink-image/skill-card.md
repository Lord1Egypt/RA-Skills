## Description: <br>
Evolink Image helps agents generate and edit images using EvoLink-supported models for text-to-image, image-to-image, and inpainting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvoLinkAI](https://clawhub.ai/user/EvoLinkAI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate, edit, inpaint, and iterate on images through EvoLink image-generation models. It also guides API-key setup, file upload, task polling, error handling, and model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source images, generated images, and API-key-backed usage are sent to EvoLink services. <br>
Mitigation: Install only if you trust EvoLink with this data, keep EVOLINK_API_KEY confidential, and avoid uploading confidential or personal images unless this use is approved. <br>
Risk: Uploaded files and generated results may be exposed through temporary public URLs. <br>
Mitigation: Treat returned file and result URLs as sensitive, share them only with intended recipients, and save needed results before their expiration windows. <br>
Risk: Using an unpinned MCP package can change runtime behavior when a new package version is published. <br>
Mitigation: Pin the MCP package version in production or controlled environments instead of using @latest. <br>


## Reference(s): <br>
- [Evolink homepage](https://evolink.ai) <br>
- [ClawHub skill page](https://clawhub.ai/EvoLinkAI/evolink-image) <br>
- [Evolink Media skill](https://clawhub.ai/EvoLinkAI/evolink-media) <br>
- [Evolink Media MCP package](https://www.npmjs.com/package/@evolinkai/evolink-media) <br>
- [Evolink Image API parameter reference](references/image-api-params.md) <br>
- [Evolink File Hosting API](references/file-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, API parameters, task status summaries, and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include temporary public file URLs and generated image result URLs with documented expiration windows.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
