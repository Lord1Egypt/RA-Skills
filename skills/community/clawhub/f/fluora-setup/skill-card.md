## Description: <br>
Interactive setup wizard for Fluora marketplace integration that clones fluora-mcp from GitHub, builds locally, generates a wallet, and configures mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chetan-guevara](https://clawhub.ai/user/chetan-guevara) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up Fluora marketplace access by cloning and building fluora-mcp, creating a local wallet, and configuring mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a crypto wallet and handles local private-key material. <br>
Mitigation: Use a small, dedicated wallet, keep only minimal funds in it, and protect the generated wallet file. <br>
Risk: The setup downloads and builds external code during installation. <br>
Mitigation: Review the cloned fluora-mcp repository before running it and avoid running the setup with elevated privileges. <br>
Risk: The setup changes persistent mcporter configuration. <br>
Mitigation: Back up or inspect mcporter.json before running the setup and review the resulting configuration. <br>


## Reference(s): <br>
- [ClawHub Fluora Setup Listing](https://clawhub.ai/chetan-guevara/fluora-setup) <br>
- [Fluora Marketplace](https://fluora.ai) <br>
- [fluora-mcp Repository](https://github.com/fluora-ai/fluora-mcp) <br>
- [Base Network](https://base.org) <br>
- [USDC](https://www.circle.com/en/usdc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance, interactive terminal prompts, shell commands, configuration changes, and JSON setup result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and git; setup may prompt for wallet funding and mcporter configuration choices.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
