## Description: <br>
Installs and configures the Agentic SPM plugin for OpenClaw using a secp256k1 keypair to authenticate with the Guardian AI API and Chromia blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ketiyohanneschromaway](https://clawhub.ai/user/ketiyohanneschromaway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install the Agentic SPM Guardian plugin, generate the required client keypair, update OpenClaw plugin configuration, and restart the gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling enforcement can affect OpenClaw gateway decisions. <br>
Mitigation: Review the exact OpenClaw configuration changes before deployment and confirm how to disable the plugin if gateway behavior needs to be restored. <br>
Risk: The generated persistent private key could be exposed through chats, logs, repositories, or insecure backups. <br>
Mitigation: Keep the private key out of shared channels and version control, store it only in the configured local path with restricted permissions, and rotate it if exposed. <br>
Risk: Installing a third-party plugin allows it to participate in gateway decision flows. <br>
Mitigation: Install only if the publisher and plugin are trusted, and review the allow-list, load path, and plugin entry before restarting the gateway. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ketiyohanneschromaway/agent-spm-setup-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup commands, OpenClaw configuration snippets, and security handling guidance for generated key material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
