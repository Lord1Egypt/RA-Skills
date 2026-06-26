## Description: <br>
Obsidian personal knowledge management workflow based on the PARA method and an automation toolchain for vault organization, Git sync, daily timeline notes, hand-drawn diagrams, and note collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajawpwinner-del](https://clawhub.ai/user/ajawpwinner-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this Chinese-language Obsidian workflow to organize note vaults with PARA, create daily notes and reusable templates, manage naming conventions, and sync notes with Git. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git sync examples and scripts can upload an entire Obsidian vault, including private notes or attachments. <br>
Mitigation: Review changes with git status before syncing, use a private repository, and add .gitignore rules for sensitive notes and attachments. <br>
Risk: The mobile Git clone example embeds an access token in a repository URL. <br>
Mitigation: Use least-privilege tokens, avoid sharing command history or screenshots that expose tokens, and rotate tokens if they are disclosed. <br>
Risk: Unattended cron-based sync can publish unreviewed vault changes. <br>
Mitigation: Prefer manual sync unless automatic full-vault uploads are intended and the vault contents have been reviewed. <br>


## Reference(s): <br>
- [PARA Method Details](references/para-method.md) <br>
- [Toolchain Configuration](references/toolchain.md) <br>
- [Template Library](references/templates.md) <br>
- [Forte Labs PARA Method](https://fortelabs.com/blog/para-method/) <br>
- [ClawHub Skill Page](https://clawhub.ai/ajawpwinner-del/awesome-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and template snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Chinese-language Obsidian vault structure guidance, note templates, Git sync steps, mobile setup notes, and optional shell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
