## Description:

Synchronizes Feishu Wiki documents into an Obsidian PARA knowledge base using a gated four-step pipeline and local SYNC-RULES.md configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink-kai](https://clawhub.ai/user/ink-kai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to import Feishu Wiki pages into a local Obsidian vault, preserve wiki hierarchy, add Feishu frontmatter, and review sync quality before accepting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-mode JSON can direct file creation outside the intended Obsidian vault if paths are manipulated.

Mitigation: Constrain scripts/sync.py so all destination paths resolve under VAULT_DIR, require basename .md filenames, and write only destinations from the cached plan.

Risk: Synced notes include Feishu document, wiki, and node identifiers in frontmatter.

Mitigation: Avoid sharing generated notes unless those Feishu identifiers are acceptable to disclose.

Risk: Automatic sync or persistent AGENTS.md additions may perform recurring local writes.

Mitigation: Enable automatic systemd sync or AGENTS.md persistence only when the user explicitly wants that behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ink-kai/skills/feishu-sync-obsidian-local)
- [Sync quality checklist](references/review-checklist.md)
- [PARA routing rules](references/routing-rules.md)
- [SYNC-RULES template](assets/sync-rules-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON inputs or outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sync plans, Obsidian Markdown files with frontmatter, write reports, and quality review guidance.]

## Skill Version(s):

1.2.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
