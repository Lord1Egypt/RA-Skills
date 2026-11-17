## Description:

Analyzes article structure, identifies useful illustration positions, and generates Type x Style article visuals for Markdown articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to analyze articles, choose illustration types and styles, generate prompt files and images, and insert Markdown image references into article drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update local Markdown articles and create backups, output folders, prompt files, image files, and persistent EXTEND.md preferences.

Mitigation: Use project-scoped preferences when possible, choose copy/update options deliberately, and review changed article files before publishing.

Risk: Generated illustrations and labels may misrepresent article content if prompts omit the article's actual terms, metrics, or claims.

Mitigation: Review the generated outline and saved prompt files before image generation, then check final Markdown image placements against the source article.

## Reference(s):

- [Baoyu Article Illustrator homepage](https://github.com/JimLiu/baoyu-skills#baoyu-article-illustrator)
- [Detailed Workflow Procedures](references/workflow.md)
- [Usage](references/usage.md)
- [Style Reference](references/styles.md)
- [Style Presets](references/style-presets.md)
- [Prompt Construction](references/prompt-construction.md)
- [First-Time Setup](references/config/first-time-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML frontmatter, prompt files, image references, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create output folders, outlines, prompt files, copied references, image files, backups, and optional EXTEND.md preferences.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence; artifact frontmatter reports 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
