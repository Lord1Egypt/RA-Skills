## Description: <br>
Analyzes article structure, identifies where visual aids are useful, and generates article illustrations using a Type, Style, and Palette workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to analyze articles, choose illustration positions, create saved image prompts, generate raster illustrations, and insert Markdown image references into the article. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill contains a prompt telling the agent not to refuse sensitive or copyrighted-figure requests. <br>
Mitigation: Review requests before generation, enforce your own content and copyright policy, or remove that prompt line before installation. <br>
Risk: The workflow stores prompts, references, generated images, backups, and preferences in local or project directories. <br>
Mitigation: Run it in an appropriate workspace, review saved files before sharing, and avoid putting sensitive article content in prompts or reference files. <br>
Risk: The evidence marks the skill as requiring sensitive credentials for image-generation backends. <br>
Mitigation: Provide credentials only through trusted environment or configuration mechanisms, scope keys narrowly, and rotate them if exposed. <br>


## Reference(s): <br>
- [Baoyu Article Illustrator homepage](https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator) <br>
- [Usage Guide](references/usage.md) <br>
- [Workflow Guide](references/workflow.md) <br>
- [Prompt Construction](references/prompt-construction.md) <br>
- [Style Presets](references/style-presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Image files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with saved prompt files, outline files, generated raster images, and optional article image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output directories containing outline.md, prompts, generated images, reference copies, backups, and optional EXTEND.md preferences; can use external image-generation backends that require credentials.] <br>

## Skill Version(s): <br>
1.117.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
