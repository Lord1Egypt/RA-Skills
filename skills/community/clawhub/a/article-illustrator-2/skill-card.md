## Description: <br>
Generate multiple illustrations for an article with structured type and style decisions and bundled generation tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[632657122](https://clawhub.ai/user/632657122) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, writers, editors, and developers use this skill to plan, generate, and insert coordinated illustrations into long-form Markdown articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article text, generated prompts, and selected reference images may be sent to WeryAI for image generation. <br>
Mitigation: Use only content approved for third-party processing and avoid private local images or sensitive drafts unless that upload is intended. <br>
Risk: The workflow can write local .image-skills configuration and may persist IMAGE_GEN_API_KEY when setup is explicitly run with key persistence. <br>
Mitigation: Review generated .image-skills files before committing them and persist API keys only in approved local or secret-management locations. <br>
Risk: The skill can modify article Markdown in place and run npx/Bun-based tooling. <br>
Mitigation: Review the insertion summary and backup file after updates, and run the workflow in a controlled project environment. <br>


## Reference(s): <br>
- [Article Illustrator ClawHub Page](https://clawhub.ai/632657122/article-illustrator-2) <br>
- [Types and Styles](references/types-and-styles.md) <br>
- [Outline Template](references/outline-template.md) <br>
- [Prompt Template](references/prompt-template.md) <br>
- [WeryAI Platform Notes](scripts/vendor/shared-image-generation/references/weryai-platform.md) <br>
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task) <br>
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated prompt files, batch JSON, image files, and updated article Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create outline.md, prompt files, batch.json, generated images, local .image-skills configuration, article backups, and compressed web assets.] <br>

## Skill Version(s): <br>
9.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
