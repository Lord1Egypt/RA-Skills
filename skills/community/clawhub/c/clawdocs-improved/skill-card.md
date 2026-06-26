## Description: <br>
OpenClaw documentation expert with config references, errata tracking, search scripts, and decision tree navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sallvainian](https://clawhub.ai/user/Sallvainian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to answer OpenClaw documentation questions, navigate configuration references, produce setup guidance, and troubleshoot configuration behavior with errata and validation reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional shell scripts may fetch OpenClaw documentation and write a local documentation cache. <br>
Mitigation: Review scripts before running them and run with normal user privileges in a workspace where local cache writes are acceptable. <br>
Risk: The skill includes install commands and high-privilege configuration examples that may enable exec, elevated access, browser control, hooks, wildcard URL fetching, or message forwarding. <br>
Mitigation: Review each command and configuration snippet before use, avoid pasting high-privilege examples blindly, and validate the security and privacy impact for the deployment. <br>
Risk: Documentation and runtime behavior may differ, causing incorrect configuration guidance. <br>
Mitigation: Check the bundled errata, apply changes incrementally, and inspect the OpenClaw reload log for unrecognized keys after configuration changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Sallvainian/clawdocs-improved) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [Agents Configuration Reference](references/agents.md) <br>
- [Channels Configuration Reference](references/channels.md) <br>
- [Gateway Configuration Reference](references/gateway.md) <br>
- [Tools Configuration Reference](references/tools.md) <br>
- [Session and Messages Configuration Reference](references/session-messages.md) <br>
- [Environment Providers Reference](references/environment-providers.md) <br>
- [OpenClaw Docs Errata](snippets/errata.md) <br>
- [Validated OpenClaw Config Snippets](snippets/validated-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite OpenClaw documentation paths and recommend local validation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; artifact package.json states 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
