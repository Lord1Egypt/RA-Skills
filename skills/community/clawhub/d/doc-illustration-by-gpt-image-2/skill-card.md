## Description: <br>
Generates technical-document illustrations, design-note infographics, and repo architecture visuals with GPT Image 2, supporting text-only prompts, style-guided reference images, and dry-run prompt review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eriklee1895](https://clawhub.ai/user/eriklee1895) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and agents use this skill to turn engineering docs, AI notes, Markdown specs, and codebase explanations into polished PNG illustrations and Markdown snippets for documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Illustration briefs, document details, and selected reference images may be sent to the configured OpenAI-compatible provider during live generation. <br>
Mitigation: Use dry-run first for private design docs, avoid secrets or confidential architecture details in prompts, and verify OPENAI_BASE_URL before live generation. <br>
Risk: The skill requires an OpenAI API key or compatible provider credential for live generation. <br>
Mitigation: Read credentials from the current shell or temporary interactive prompt only, and do not write credentials to disk. <br>
Risk: JSON sidecars can contain prompts, briefs, reference image paths, and project context. <br>
Mitigation: Review and delete JSON sidecars when they contain sensitive project information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eriklee1895/doc-illustration-by-gpt-image-2) <br>
- [OpenAI image workflow](references/openai-image-workflow.md) <br>
- [OpenAI official links](references/openai-official-links.md) <br>
- [Prompt patterns](references/prompt-patterns.md) <br>
- [Style profiles](references/style-profiles.md) <br>
- [GPT Image 2 model page](https://developers.openai.com/api/docs/models/gpt-image-2) <br>
- [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation) <br>
- [Python image generation reference](https://developers.openai.com/api/reference/python/resources/images/methods/generate) <br>
- [Python image editing reference](https://developers.openai.com/api/reference/python/resources/images/methods/edit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; live runs save PNG images and JSON metadata sidecars.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode emits prompt and request metadata without calling the image API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
