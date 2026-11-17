## Description:

Uses Doubao, Kimi, or ChatGPT to research a user question, organize the result, and save it as an Obsidian-ready Markdown document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alphalpha7](https://clawhub.ai/user/alphalpha7)

### License/Terms of Use:


## Use Case:

External users can use this skill to research questions with named AI services and turn the results into structured Obsidian notes with frontmatter, headings, source labels, and saved Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries may be sent to third-party AI services.

Mitigation: Confirm that the query content is appropriate to share with the selected AI service before use.

Risk: Generated notes may contain incorrect, incomplete, or poorly sourced content.

Mitigation: Review the Markdown and source labels before saving the note into the Obsidian vault.

Risk: A raw or unconfirmed file move can save content to the wrong vault path or mishandle paths with spaces.

Mitigation: Specify the exact vault and folder, quote paths, and confirm the destination before moving generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alphalpha7/skills/ai-research-to-obsidian)
- [Obsidian Markdown template](references/obsidian-template.md)
- [Doubao](https://www.doubao.com)
- [Kimi](https://kimi.moonshot.cn)
- [ChatGPT](https://chat.openai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with YAML frontmatter and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-specified Obsidian vault and folder before moving generated files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
