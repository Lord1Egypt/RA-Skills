## Description:

Analyzes article structure, identifies positions requiring visual aids, and guides an agent through generating Type x Style illustrations for articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxw975](https://clawhub.ai/user/gxw975)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and content-focused developers use this skill to analyze an article, choose illustration density and style, draft image prompts, generate supporting visuals, and insert Markdown image links into the article.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update the target article with Markdown image links.

Mitigation: Run it on a copy or under version control when in-place article edits are not acceptable.

Risk: The skill can create illustration directories, outline files, prompt files, and generated image files.

Mitigation: Review the output directory and generated files before publishing or merging the article.

Risk: The skill may read scoped Baoyu preference files when present.

Mitigation: Review project and user preference files before use so the agent follows intended configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gxw975/skills/clawhub-publish-146256)
- [Baoyu Article Illustrator homepage](https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, file paths, outline entries, prompt files, and article image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an illustrations directory containing source copies, references, outline.md, prompt files, and generated image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
