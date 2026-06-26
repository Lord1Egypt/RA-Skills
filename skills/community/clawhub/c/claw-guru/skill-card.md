## Description: <br>
OpenClaw support skill for troubleshooting configuration errors, gateway startup and crashes, chat channel routing, integrations, authentication, upgrades, tools, policies, remote access, and other OpenClaw topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isriam](https://clawhub.ai/user/isriam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and resolve OpenClaw gateway, configuration, integration, routing, authentication, installation, and upgrade problems using live documentation and local diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic workflows may read OpenClaw logs, installed files, and configuration paths that can contain private operational details or tokens. <br>
Mitigation: Review diagnostic output before sharing it and redact sensitive values from logs or configuration snippets. <br>
Risk: Configuration edits or gateway restarts can disrupt an OpenClaw installation if applied without review. <br>
Mitigation: Back up the configuration, validate JSON, and review proposed edits or restart commands before allowing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/isriam/claw-guru) <br>
- [OpenClaw docs home](https://docs.openclaw.ai) <br>
- [OpenClaw docs index](https://docs.openclaw.ai/llms.txt) <br>
- [OpenClaw configuration reference](https://docs.openclaw.ai/gateway/configuration-reference.md) <br>
- [OpenClaw gateway troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting.md) <br>
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw) <br>
- [OpenClaw GitHub issues](https://github.com/openclaw/openclaw/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose diagnostic commands, log review, configuration validation steps, and gateway restart guidance for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
