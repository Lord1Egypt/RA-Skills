## Description: <br>
Guides agents through ricebowl.ai image-generation workflows, including model selection, API-key setup, text-to-image or image-to-image commands, and result retrieval with the ai-media CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinchanzis](https://clawhub.ai/user/jinchanzis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to configure the ai-media CLI and run ricebowl.ai image-generation workflows from prompts or reference images. It helps select models, set API credentials, generate images, and fetch completed task outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image generation can consume paid credits or quota on ricebowl.ai. <br>
Mitigation: Confirm the selected model, prompt, and expected cost before running generation commands, especially with --wait or repeated task execution. <br>
Risk: The workflow requires API-key configuration for AI_MEDIA_API_KEY and may use a configurable base URL. <br>
Mitigation: Use a dedicated API key where possible, verify AI_MEDIA_BASE_URL before use, and avoid pasting secrets into shared logs or transcripts. <br>
Risk: Some command examples and workflow notes are written in Chinese, which can lead to misconfiguration for readers who do not understand them. <br>
Mitigation: Review command flags and model parameters before execution, and translate unclear examples before using them in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinchanzis/ai-media-generator-ai-image-generation) <br>
- [Project homepage](https://github.com/214140846/ai-media-generator) <br>
- [Publisher profile](https://clawhub.ai/user/jinchanzis) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI commands that use AI_MEDIA_API_KEY, AI_MEDIA_BASE_URL, model names, prompts, aspect ratios, image URLs, and task IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
