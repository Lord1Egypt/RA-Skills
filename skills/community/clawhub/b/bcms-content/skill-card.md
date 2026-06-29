## Description: <br>
Run BCMS content operations from the command line with a thin CLI that lets agents create, update, delete, and list entries and upload media using a BCMS API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bcms](https://clawhub.ai/user/bcms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, editors, and agent operators use this skill to run deterministic BCMS entry and media operations from terminals, CI jobs, and agent workflows. It is intended for content tasks where command output and JSON results are preferable to interactive dashboard work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive BCMS API key that can be exposed through repository configs, logs, browser history, shared config, or chat. <br>
Mitigation: Use a dedicated least-privilege key from environment variables or a secret manager, keep keys out of repo configs, and rotate any key that may have been exposed. <br>
Risk: The CLI can change or delete CMS content when the provided key has content-management permissions. <br>
Mitigation: Scope keys to the needed templates and operations, confirm entry IDs with list commands before deletes, and avoid production delete permissions unless they are required. <br>


## Reference(s): <br>
- [BCMS Content Skill Page](https://clawhub.ai/bcms/bcms-content) <br>
- [BCMS Agent Setup Guide](https://thebcms.com/agents) <br>
- [BCMS Documentation](https://thebcms.com/docs) <br>
- [BCMS MCP Guide](https://thebcms.com/docs/mcp) <br>
- [BCMS Entries](references/entries.md) <br>
- [BCMS Media](references/media.md) <br>
- [BCMS Permissions](references/permissions.md) <br>
- [BCMS Properties](references/properties.md) <br>
- [BCMS Model Context Protocol](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; CLI runs print a short status line followed by JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scoped BCMS API key and can modify or delete BCMS content when the key has those permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
