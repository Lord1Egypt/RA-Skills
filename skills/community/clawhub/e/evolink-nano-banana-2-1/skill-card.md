## Description: <br>
Nano Banana 2 is an Evolink image-generation skill for fast text-to-image and image-editing workflows using Google Gemini 3.1 Flash through the Evolink API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bethune89](https://clawhub.ai/user/Bethune89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create or edit images through Evolink, configure an Evolink API key, upload reference images when needed, and poll asynchronous image-generation tasks until completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and images to Evolink services and may expose temporary public links for generated or uploaded files. <br>
Mitigation: Avoid confidential prompts or images unless the user accepts Evolink processing and temporary public URL exposure; save needed results before their URLs expire. <br>
Risk: The Evolink API key authenticates image generation and file operations. <br>
Mitigation: Use a dedicated Evolink API key, keep it confidential, and rotate or revoke it if exposure is suspected. <br>
Risk: The workflow can rely on an external MCP npm package. <br>
Mitigation: Verify or pin the MCP package version before use instead of blindly relying on an unpinned latest package. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bethune89/evolink-nano-banana-2-1) <br>
- [Evolink homepage](https://evolink.ai) <br>
- [Focused full Evolink image skill](https://clawhub.ai/EvoLinkAI/evolink-image) <br>
- [Evolink media MCP package](https://www.npmjs.com/package/@evolinkai/evolink-media) <br>
- [Nano Banana 2 image API parameter reference](references/image-api-params.md) <br>
- [Evolink file hosting API reference](references/file-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, tool-call instructions, URLs, and task status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce temporary public image and file URLs from Evolink services; generated result URLs expire after 24 hours and uploaded files expire after 72 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
