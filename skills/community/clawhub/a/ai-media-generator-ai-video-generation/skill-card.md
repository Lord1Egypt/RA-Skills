## Description: <br>
Use when someone asks for AI video generation, video generator, text-to-video, image-to-video, prompt-to-video, video model selection, or CLI-based video workflows on ricebowl.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinchanzis](https://clawhub.ai/user/jinchanzis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to select ricebowl.ai video models, configure ai-media CLI credentials, and generate or retrieve text-to-video and image-to-video jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing and using the ai-media-generator CLI package. <br>
Mitigation: Install only if the package and ricebowl.ai account workflow are trusted. <br>
Risk: The workflow uses AI_MEDIA_API_KEY for video-generation API access. <br>
Mitigation: Use a dedicated API key and avoid exposing it in shared terminals, screenshots, chat logs, or shell history. <br>
Risk: Video generation may consume account credits based on model, duration, and prompt choices. <br>
Mitigation: Confirm the selected model, duration, prompt, and credit cost before generating videos. <br>


## Reference(s): <br>
- [ai-media-generator homepage](https://github.com/214140846/ai-media-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI commands for ai-media configuration, model inspection, video generation, polling, and task retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
