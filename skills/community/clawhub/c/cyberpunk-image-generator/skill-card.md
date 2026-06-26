## Description: <br>
Generate cyberpunk style futuristic art. Use when the user asks for neon, sci-fi, dystopia, or cyberpunk cityscapes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate cyberpunk, neon, sci-fi, dystopian, or cityscape artwork through a WeryAI-backed image-generation workflow. It guides setup, model selection, prompt construction, batch generation, and output delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist an image-generation API key and modify project configuration. <br>
Mitigation: Use a dedicated low-privilege API key, prefer a secure environment or secret store over project .env persistence, and review setup prompts before approving changes. <br>
Risk: The skill may install local tooling before generation. <br>
Mitigation: Install only after reviewing the setup request and only when the publisher and WeryAI integration are trusted. <br>
Risk: Prompts, reference images, webhook callbacks, or web-search options may send data to external services. <br>
Mitigation: Avoid sensitive local files or confidential prompt content, and enable webhook or web-search options only when the destination and data flow are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/632657122/cyberpunk-image-generator) <br>
- [Gateway Alignment Notes](references/weryai-platform.md) <br>
- [First-Time Setup](references/config/first-time-setup.md) <br>
- [Model Registry Schema](references/config/model-registry-schema.md) <br>
- [Preferences Schema](references/config/preferences-schema.md) <br>
- [Style Presets](references/style-presets.md) <br>
- [WeryAI API documentation](https://docs.weryai.com/en) <br>
- [WeryAI text-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task) <br>
- [WeryAI image-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task) <br>
- [WeryAI task status API](https://docs.weryai.com/api-reference/tasks/query-task-details) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, local configuration files, downloaded image files, and optional JSON summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY and a local Node/npm runtime; generated images are delivered as files or usable image URLs when inline display is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
