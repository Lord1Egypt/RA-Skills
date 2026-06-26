## Description: <br>
Save, retrieve, and manage notes using the Dnote CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[M1n-74316D65](https://clawhub.ai/user/M1n-74316D65) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and note-taking users use this skill to capture, search, organize, edit, export, and sync Dnote notes from agent workflows. It is suited for maintaining a personal knowledge base of commands, snippets, journal entries, and task-specific notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete individual notes or entire books, including through commands that pass confirmation flags. <br>
Mitigation: Require explicit user confirmation before running remove or remove-book commands, and keep backups for important Dnote databases. <br>
Risk: Dnote notes, exports, sync operations, and configuration output can expose private or business-critical information. <br>
Mitigation: Use local-only mode unless cloud sync is intentional, avoid storing secrets in notes or config, and review note or config output before sharing it with an agent. <br>
Risk: The setup guidance includes a curl-to-shell installer path. <br>
Mitigation: Prefer Homebrew or verified Dnote release downloads when installing the required CLI. <br>


## Reference(s): <br>
- [Dnote CLI documentation](https://www.getdnote.com/docs/cli/) <br>
- [Dnote CLI installation documentation](https://www.getdnote.com/docs/cli/installation/) <br>
- [Dnote GitHub releases](https://github.com/dnote/dnote/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and Dnote text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the dnote CLI; supports DNOTE_DB_PATH for selecting a local database and optional DNOTE_API_KEY or Dnote login for sync.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
