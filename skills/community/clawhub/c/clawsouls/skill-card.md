## Description: <br>
Manage AI agent personas, called Souls, for OpenClaw by helping users install, switch, list, restore, create, validate, publish, and synchronize persona packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TomLeeLive](https://clawhub.ai/user/TomLeeLive) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and external OpenClaw users use this skill to manage persona packages that change an agent's identity, behavior, style, and workspace configuration. It supports installing and activating existing personas, restoring prior personas, creating new persona packages, validating them, publishing them, and synchronizing encrypted memory when the ClawSouls CLI is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote memory sync may synchronize sensitive prompts, memory, or client data. <br>
Mitigation: Review exactly which files will be synchronized before running sync or swarm commands, and avoid using them in workspaces containing sensitive data unless the user has approved the scope. <br>
Risk: Publishing or synchronization can upload local persona or memory content outside the workspace. <br>
Mitigation: Run publish or sync only after confirming the destination, selected files, and user intent. <br>
Risk: CLAWSOULS_TOKEN can be exposed through shell history, logs, or commits. <br>
Mitigation: Keep the token out of committed files and persistent shell history, and prefer secure environment management. <br>
Risk: The skill relies on an external ClawSouls npm CLI that may change behavior across versions. <br>
Mitigation: Prefer trusted or pinned CLI versions and review commands before execution. <br>
Risk: Activating a Soul persistently changes agent identity and behavior files. <br>
Mitigation: Use the built-in backup and restore flow, restart the gateway only after an intentional switch, and start a new chat session to avoid mixed persona context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TomLeeLive/clawsouls) <br>
- [ClawSouls Registry](https://clawsouls.ai) <br>
- [ClawSouls npm Package](https://www.npmjs.com/package/clawsouls) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Soul-Driven Interaction Design](https://doi.org/10.5281/zenodo.18772585) <br>
- [Soul Spec MCP](https://github.com/clawsouls/soul-spec-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workspace-changing CLI instructions for persona files, backups, publishing, validation, and encrypted memory synchronization.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
