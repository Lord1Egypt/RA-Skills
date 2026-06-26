## Description: <br>
Helps configure two Discord bots on one machine with isolated workspaces, channel allowlists, mention-gated reviewer behavior, optional one-way reviewer feedback, and backup/rollback commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nbdxrycyl](https://clawhub.ai/user/nbdxrycyl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure a primary Discord bot and reviewer bot, tune reply rules, and recover from bad configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can rewrite persistent bot configuration using loosely validated paths and values. <br>
Mitigation: Review the scripts before running them, use trusted simple paths and numeric Discord IDs, and create a backup before applying policy or rollback changes. <br>
Risk: Discord bot tokens or backed-up configuration could be exposed if stored in shared locations. <br>
Mitigation: Keep real tokens out of shared files, store secrets and backups in private directories, and limit access to generated .env and backup files. <br>
Risk: Untrusted channel or configuration values could lead to unsafe configuration changes. <br>
Mitigation: Use only trusted channel and config values until stronger input validation is added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nbdxrycyl/discord-dual-bot-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell command snippets and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Placeholder-based; users must replace Discord bot, guild, channel, and path values before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
