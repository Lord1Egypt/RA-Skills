## Description: <br>
Installs, configures, and helps users use Corust Agent (corust-agent-acp), an ACP-compatible coding agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phoenix500526](https://clawhub.ai/user/phoenix500526) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install corust-agent-acp, configure ACPX and OpenClaw integration, and provide Discord setup guidance while preserving existing agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Discord access can let untrusted users trigger a powerful coding agent. <br>
Mitigation: Use a narrow Discord allowlist for specific trusted servers, channels, roles, or users before enabling ACP thread spawning. <br>
Risk: Approve-all permission mode can allow agent actions without enough review in an untrusted environment. <br>
Mitigation: Avoid approve-all unless the environment is fully trusted, keep non-interactive permissions denied, and review proposed changes before execution. <br>
Risk: Installing the latest release archive can introduce unverified binary code. <br>
Mitigation: Verify the downloaded Corust release and source before installing or updating the binary. <br>
Risk: Configuration edits can overwrite existing OpenClaw or ACPX settings. <br>
Mitigation: Back up existing configuration and merge the Corust entries instead of replacing unrelated sections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phoenix500526/corust-agent) <br>
- [Corust Agent release archive referenced by the skill](https://github.com/Corust-ai/corust-agent-release/releases/latest/download/agent-darwin-arm64.tar.gz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation steps, merge-safe configuration guidance, troubleshooting notes, and Discord setup instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
