## Description:

Article Organizer Builder helps agents create a customized Obsidian article-organizer skill that turns saved web or WeChat articles into structured notes with tags, backlinks, a single MOC index, deduplication, and safe source archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kakahilda](https://clawhub.ai/user/kakahilda)

### License/Terms of Use:

MIT-0

## Use Case:

Obsidian users and agent-skill builders use this skill to generate a reusable article collection workflow tailored to their vault paths, categories, tags, and note title preferences. The generated skill scans source articles, proposes deduplication and classification, writes structured Markdown notes, updates one index page, and archives processed source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated organizer may move processed source articles and attachment folders into an archive or recycle location.

Mitigation: Review the generated source, archive, and cleanup paths before running it on important notes, and confirm archived contents before deleting anything manually.

Risk: The builder creates a persistent local skill under the user's skills directory.

Mitigation: Review the generated skill files, path boundaries, and cleanup behavior before enabling or using the generated organizer.

Risk: Incorrect custom paths or broad classification rules can organize notes in unexpected locations or categories.

Mitigation: Confirm the four directory settings, category rules, and tag mappings during setup, then run the generated scan report before writing or cleaning up notes.

## Reference(s):

- [Builder Prompt](references/builder-prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/kakahilda/skills/article-organizer-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated skill files and Python standard-library scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a local skill directory from user-provided vault paths, classification rules, tag mappings, and title preferences.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
