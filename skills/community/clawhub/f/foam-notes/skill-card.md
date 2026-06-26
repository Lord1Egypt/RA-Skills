## Description: <br>
Helps agents work with Foam Markdown note repositories by creating, editing, linking, tagging, searching, and summarizing notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hegghammer](https://clawhub.ai/user/Hegghammer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to manage local Foam workspaces, create and organize Markdown notes, inspect backlinks and tags, and apply wikilink or tag suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local Markdown notes and templates, including deleting notes, renaming files, fixing links, and applying tag or wikilink suggestions. <br>
Mitigation: Set foam_root or FOAM_WORKSPACE to the intended notes folder, keep backups or version control, and review changes before using delete, rename, --force, --fix-links, --auto-apply, or broad tag/link application options. <br>
Risk: Workspace auto-detection may target the wrong notes folder if configuration is unset. <br>
Mitigation: Prefer an explicit --foam-root argument, FOAM_WORKSPACE value, or config.json foam_root when operating on important workspaces. <br>
Risk: Automated wikilink and tag suggestions may add links or tags that do not match the user's intended organization. <br>
Mitigation: Use dry-run or interactive selection modes first, then review resulting Markdown changes before accepting them. <br>


## Reference(s): <br>
- [Foam Notes release page](https://clawhub.ai/Hegghammer/foam-notes) <br>
- [Foam Documentation Overview](artifact/references/foam-overview.md) <br>
- [Foam Notes Configuration](artifact/references/configuration.md) <br>
- [Wikilinks in Foam](artifact/references/wikilinks.md) <br>
- [Backlinks in Foam](artifact/references/backlinks.md) <br>
- [Tags in Foam](artifact/references/tags.md) <br>
- [Daily Notes in Foam](artifact/references/daily-notes.md) <br>
- [Templates in Foam](artifact/references/templates.md) <br>
- [Foam official site](https://foamnotes.com) <br>
- [Foam project repository](https://github.com/foambubble/foam) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local Markdown/configuration file changes when scripts are used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on a local Foam workspace selected by --foam-root, FOAM_WORKSPACE, config.json, auto-detection, or current working directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
