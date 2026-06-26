## Description: <br>
AI-powered presentation generation using the 2slides API for creating slides from text, reference images, or documents, with theme selection, multilingual support, export workflows, and voice narration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create, export, and narrate presentation decks from text, documents, or reference images through the 2slides service. It is useful when an agent needs to guide slide generation workflows, choose themes, check asynchronous job status, or retrieve presentation outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide content, document-derived summaries, reference image URLs or base64 images, job IDs, and related metadata are sent to the third-party 2slides service. <br>
Mitigation: Install and use the skill only when that data sharing is acceptable for the intended presentation content. <br>
Risk: The 2slides API key is required for generation and could grant access to paid credits if exposed. <br>
Mitigation: Treat the API key as a secret and prefer environment-based secret storage over embedding credentials in URLs or shared configuration files. <br>
Risk: Download output paths can overwrite existing local files if chosen carelessly. <br>
Mitigation: Use explicit output paths and review destination filenames before downloading slide, voice, or transcript archives. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/javainthinking/2slides-skills) <br>
- [2slides API](https://2slides.com/api) <br>
- [2slides Pricing](https://2slides.com/pricing) <br>
- [API Reference](references/api-reference.md) <br>
- [MCP Integration](references/mcp-integration.md) <br>
- [Pricing](references/pricing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, configuration snippets, and generated file links from the service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference slide URLs, PDF URLs, job IDs, ZIP downloads, PNG slide pages, WAV narration files, and transcripts produced by 2slides.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
