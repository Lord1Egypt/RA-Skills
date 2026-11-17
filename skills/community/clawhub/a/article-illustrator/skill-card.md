## Description:

Analyzes article structure, identifies positions for visual aids, and generates illustrations using a Type x Style two-dimension approach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Writers, editors, and content teams use this skill to add relevant visual aids to articles or blog posts. It analyzes the content, recommends illustration positions, confirms type, density, and style, then produces an outline, image prompts, generated illustrations, and Markdown image references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags an instruction that tries to suppress image-generation refusals for sensitive or copyrighted subjects.

Mitigation: Review generated prompts before image generation and remove or override instructions that conflict with content policy or rights requirements.

Risk: The security evidence notes mutable install commands.

Mitigation: Install from a reviewed release or pinned commit, and review the skill contents before deployment.

Risk: The skill can read article content, create illustration files, save optional preferences, and update article Markdown.

Mitigation: Use the documented confirmation steps before file changes, and review generated file paths and Markdown edits before accepting them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wpank/skills/article-illustrator)
- [Usage](references/usage.md)
- [Style Reference](references/styles.md)
- [Prompt Construction](references/prompt-construction.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [First-Time Setup](references/config/first-time-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML frontmatter examples, shell commands, image prompts, file paths, and Markdown image references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create illustration outlines, prompt files, generated image files, optional preferences, and updated article Markdown after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter); release package version 0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
