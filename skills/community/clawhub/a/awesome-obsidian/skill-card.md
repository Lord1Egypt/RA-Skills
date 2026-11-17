## Description:

Obsidian personal knowledge management workflow based on the PARA method and automation tooling for organizing vault structure, Git sync, daily timeline notes, hand-drawn diagrams, and collected notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajawpwinner-del](https://clawhub.ai/user/ajawpwinner-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to structure and maintain an Obsidian vault with PARA folders, reusable note templates, daily logs, and Git-based synchronization. It is most useful for personal knowledge management workflows that need repeatable organization, review, and backup practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git synchronization guidance can upload all unignored vault contents, including private notes or local files.

Mitigation: Use the skill only with an intended private vault, maintain a strict .gitignore, and inspect git status and staged diffs before pushing.

Risk: Embedding access tokens in clone URLs can expose credentials in shell history, configuration, or logs.

Mitigation: Avoid token-bearing clone URLs and prefer SSH authentication or a credential manager.

Risk: Unattended cron synchronization can push unintended changes without review.

Mitigation: Enable automated sync only after confirming that unattended uploads of all unignored vault contents are acceptable.

## Reference(s):

- [PARA Method Reference](references/para-method.md)
- [Toolchain Configuration](references/toolchain.md)
- [Template Library](references/templates.md)
- [Fortelabs PARA Method](https://fortelabs.com/blog/para-method/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file organization guidance, Obsidian template content, Git commands, and synchronization recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
