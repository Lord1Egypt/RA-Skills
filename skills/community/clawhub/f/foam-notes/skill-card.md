## Description:

Work with Foam note repositories. Create, edit, link, and tag notes. Get intelligent wikilink and tag suggestions. Skill supports backlinks discovery, daily notes, templates, graph visualization, note deletion, and renaming. Full Foam documentation included for easy querying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hegghammer](https://clawhub.ai/user/hegghammer)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Foam-based Markdown knowledge bases: creating notes, daily notes, templates, wikilinks, backlinks, tags, and graph summaries. It is useful for agents that need to inspect or update local Foam workspaces while preserving Foam conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can create, modify, rename, or delete local Markdown notes, and the security review warns that some operations may affect files outside the intended Foam workspace.

Mitigation: Set the Foam root explicitly, review resolved paths before execution, keep backups or version control enabled, and avoid untrusted note names or paths.

Risk: Force or automatic-apply modes can bypass interactive review for destructive deletes, renames, wikilink insertion, or tag insertion.

Mitigation: Avoid --force and --auto-apply for normal use; preview suggestions and apply only selected changes after review.

Risk: Deleting or renaming notes can change backlinks and linked notes in ways that are difficult to unwind.

Mitigation: Use backup mode for deletion, inspect affected backlinks before confirming, and review workspace diffs after the command finishes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hegghammer/skills/foam-notes)
- [Foam official site](https://foamnotes.com)
- [Foam GitHub repository](https://github.com/foambubble/foam)
- [Foam overview](references/foam-overview.md)
- [Wikilinks](references/wikilinks.md)
- [Backlinks](references/backlinks.md)
- [Tags](references/tags.md)
- [Daily notes](references/daily-notes.md)
- [Templates](references/templates.md)
- [Configuration](references/configuration.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text guidance with inline shell commands; local scripts may produce Markdown files, JSON summaries, or workspace file edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill operates on local Foam workspaces and may create, update, rename, or delete Markdown notes when its scripts are run.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
