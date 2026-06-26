## Description: <br>
Encrypted Docs lets agents and people create, search, update, sync, share, and delete end-to-end encrypted Markdown documents through a Fileverse MCP/API server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vijaykrishnavanshi](https://clawhub.ai/user/vijaykrishnavanshi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and document collaborators use this skill to connect an agent to a trusted Fileverse server for encrypted Markdown document creation, search, updates, sync status checks, sharing, and deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Share links include key material and can grant document access. <br>
Mitigation: Treat ddoc links as secrets and share them only with people or agents that should have access. <br>
Risk: Deleting or overwriting the wrong document can permanently remove important content. <br>
Mitigation: Confirm the exact document identifier and user intent before delete or overwrite operations. <br>
Risk: The connector depends on the configured Fileverse server. <br>
Mitigation: Install and use it only with a Fileverse server URL the user operates or trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vijaykrishnavanshi/encrypted-docs) <br>
- [ddocs.new](https://ddocs.new) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns document metadata, sync status, content, and share links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
