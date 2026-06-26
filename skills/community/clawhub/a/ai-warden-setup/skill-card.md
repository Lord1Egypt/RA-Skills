## Description: <br>
Install, configure, and manage the AI-Warden prompt injection protection plugin for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-warden](https://clawhub.ai/user/ai-warden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install or update AI-Warden, configure shields and API-key options, verify status, and troubleshoot plugin issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent OpenClaw plugin that can change agent security behavior. <br>
Mitigation: Install only if the AI-Warden publisher is trusted, and verify the npm package name, version, repository, and checksum before enabling it. <br>
Risk: The setup changes local OpenClaw configuration and extension files. <br>
Mitigation: Keep the configuration backup, review the proposed changes before restart, and restore the backup if the gateway fails after installation. <br>
Risk: Using online detection may involve third-party data handling and an API key. <br>
Mitigation: Prefer the environment-variable API-key option and review AI-Warden data-handling terms before enabling online detection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-warden/ai-warden-setup) <br>
- [AI-Warden website](https://ai-warden.io) <br>
- [openclaw-ai-warden npm package](https://www.npmjs.com/package/openclaw-ai-warden) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands to install the npm package, update OpenClaw configuration, set an optional API key, restart the gateway, and verify status.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
