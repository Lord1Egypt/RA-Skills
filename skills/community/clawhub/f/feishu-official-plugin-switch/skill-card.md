## Description: <br>
Guides an OpenClaw Feishu deployment through switching from the community plugin to the official Feishu plugin, including streaming output, user identity features, and diagnostic commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan and validate an OpenClaw Feishu plugin migration, review required Feishu permissions, and collect the commands needed for installation, configuration, restart, and diagnostics. The implementation returns guidance and status-style messages rather than independently proving that those system changes occurred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can report installation, configuration, restart, and verification steps as successful even when those actions were not actually executed or checked. <br>
Mitigation: Treat responses as an instructional checklist; manually run and verify each OpenClaw and Feishu command before relying on the migration state. <br>
Risk: Suggested package installation and OpenClaw configuration commands may affect the local gateway or plugin setup. <br>
Mitigation: Use a pinned and trusted package version, avoid sudo unless necessary, and back up the current plugin configuration before applying changes. <br>
Risk: The documented Feishu permissions include broad user and tenant scopes for advanced features. <br>
Mitigation: Grant only the Feishu scopes required for the intended features and review authorization choices before enabling user-identity operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rfdiosuao/feishu-official-plugin-switch) <br>
- [Official Feishu plugin guide](https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Referenced GitHub README](https://github.com/rfdiosuao/openclaw-skills/blob/main/feishu-official-plugin-switch/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown text with bash and TypeScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns instructional status reports, next-action labels, permission examples, troubleshooting steps, and diagnostic commands.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata, skill.json, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
