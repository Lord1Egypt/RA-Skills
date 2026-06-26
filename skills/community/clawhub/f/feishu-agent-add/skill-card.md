## Description: <br>
Use this skill when users want to add a Feishu agent for OpenClaw, including guided prompt flows and one-command generation of the matching OpenClaw configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyecho-io](https://clawhub.ai/user/cyecho-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to add a Feishu-connected agent, collect the required app credentials, preview the planned changes, update local OpenClaw configuration, and initialize a workspace when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret can be exposed when supplied with the --app-secret command-line flag. <br>
Mitigation: Prefer the interactive hidden prompt or another protected secret method, and avoid pasting secrets into shell history. <br>
Risk: The execution script can make persistent changes to local OpenClaw configuration and workspace files. <br>
Mitigation: Run --dry-run first, review the preview, and rely on the generated backup before applying changes. <br>
Risk: Agent-to-agent collaboration may broaden the new bot's interaction surface if enabled by default. <br>
Mitigation: Use --disable-agent-to-agent unless the Feishu agent needs collaboration with other agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyecho-io/feishu-agent-add) <br>
- [Publisher profile](https://clawhub.ai/user/cyecho-io) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent local OpenClaw configuration and workspace files when the execution script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
