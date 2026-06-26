## Description: <br>
Generate chalkboard art and chalk drawings. Use when the user asks for chalk art, blackboard menu, or pastel drawing on dark background. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate chalkboard-style images, blackboard menu art, and pastel drawings on dark backgrounds through a WeryAI image-generation gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist configuration and API credentials in local project or home skill directories. <br>
Mitigation: Use a scoped, revocable WeryAI API key and avoid persisting it to project files unless the workspace is trusted. <br>
Risk: The skill can call the WeryAI gateway and optionally use webhooks or web search. <br>
Mitigation: Enable webhooks or web search only when external sharing is intended, and review setup/bootstrap actions before approving them. <br>
Risk: The security verdict says the release needs review because it is broader and more persistent than a simple chalk-art tool. <br>
Mitigation: Review and scan the skill before installing or deploying it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/632657122/chalk-art-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/632657122) <br>
- [WeryAI platform notes](references/weryai-platform.md) <br>
- [First-time setup](references/config/first-time-setup.md) <br>
- [Model registry schema](references/config/model-registry-schema.md) <br>
- [Style presets](references/style-presets.md) <br>
- [WeryAI API documentation](https://docs.weryai.com/en) <br>
- [WeryAI text-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task) <br>
- [WeryAI image-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task) <br>
- [WeryAI task status API](https://docs.weryai.com/api-reference/tasks/query-task-details) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated image file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can submit text-to-image or image-to-image jobs, poll for completion, download result images, and manage local model/default configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 0.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
