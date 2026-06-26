## Description: <br>
Interact with Confluence Cloud from the command line when reading, creating, updating, or searching Confluence pages, managing attachments, labels, comments, or exporting content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hochej](https://clawhub.ai/user/hochej) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and documentation maintainers use this skill to work with Confluence Cloud pages and related resources from an agent-assisted command-line workflow. It helps agents check authentication, suggest safe confcli commands, and handle read, search, export, and explicitly requested write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users or agents to run a remote installer for a CLI that can change or delete Confluence content. <br>
Mitigation: Prefer a pinned confcli release, Cargo install, or an inspected downloaded installer before use. <br>
Risk: Confluence credentials with broad permissions could allow unnecessary write, delete, or purge actions. <br>
Mitigation: Use a Confluence token limited to the spaces and permissions required, and avoid broad write or delete permissions unless those workflows are needed. <br>
Risk: Write operations such as create, update, delete, purge, attachment changes, comments, labels, and copy-tree can modify workspace content. <br>
Mitigation: Require explicit user intent for write operations and use dry-run previews for destructive or bulk changes where supported. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hochej/confluence-cli) <br>
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) <br>
- [confcli Installer Script](https://raw.githubusercontent.com/hochej/confcli/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and confcli command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference confcli output modes such as JSON, table, and Markdown.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
