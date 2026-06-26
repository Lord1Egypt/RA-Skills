## Description: <br>
Read and write Obsidian notes stored in an EVC Team Relay collaborative vault through REST API helper scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[venturecrew](https://clawhub.ai/user/venturecrew) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let an AI agent list, read, create, update, and delete Markdown notes in shared EVC Team Relay Obsidian vaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an authenticated agent read, write, and delete access to configured Team Relay vault shares. <br>
Mitigation: Install with a Relay account scoped only to the shares the agent should access, prefer read-only credentials unless edits are required, and require human approval for deletes or broad updates. <br>
Risk: Relay credentials or tokens could be exposed if passed through unsafe configuration or command-line usage. <br>
Mitigation: Use RELAY_TOKEN or a protected secret source, and avoid committing RELAY_PASSWORD in configuration. <br>


## Reference(s): <br>
- [EVC Team Relay repository](https://github.com/entire-vc/evc-team-relay) <br>
- [API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/venturecrew/evc-team-relay) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, RELAY_CP_URL, and Relay authentication credentials or token.] <br>

## Skill Version(s): <br>
1.1.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
