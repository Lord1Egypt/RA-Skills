## Description:

Logs daily meals to a fixed-format Markdown file in an Obsidian vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-zzl](https://clawhub.ai/user/leo-zzl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to record breakfast, lunch, dinner, or snack entries and save them as structured daily diet notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The file-writing script can be steered to overwrite files outside the intended Obsidian folder.

Mitigation: Validate dates, reject path separators, avoid following symlinks, and constrain writes to the intended Obsidian daily-notes directory before running it on untrusted meal-log requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leo-zzl/skills/diet-logger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown notes and command-line script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes meal entries to dated Markdown files in a configured Obsidian daily-notes directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
