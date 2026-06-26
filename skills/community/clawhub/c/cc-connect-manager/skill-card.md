## Description: <br>
Manage cc-connect projects by adding projects to ~/.cc-connect/config.toml, setting up multi-agent relay bindings, and restarting cc-connect in tmux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zgq233333](https://clawhub.ai/user/zgq233333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect local agent workspaces to chat platforms through cc-connect, manage project entries, and coordinate multiple agent bots in shared channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bot credentials may be written to or displayed from cc-connect configuration. <br>
Mitigation: Use dedicated low-privilege bot tokens, redact secrets from displayed config, and avoid sharing the resulting ~/.cc-connect/config.toml. <br>
Risk: The skill can make persistent chat-to-agent configuration changes and relay bindings. <br>
Mitigation: Back up ~/.cc-connect/config.toml before changes, restrict chat groups and allowlists, and know how to remove relay bindings. <br>
Risk: Agent permission modes such as full-auto, yolo, or bypassPermissions can increase the impact of chat-controlled workspace actions. <br>
Mitigation: Avoid elevated automation modes unless they are required and trusted for the specific workspace. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and TOML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local cc-connect configuration changes and tmux restart commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
