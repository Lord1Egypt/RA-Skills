## Description:

Connects agents to Alibaba Cloud Agent Data Gateway (Dgate) through managed MCP configuration or local Dgate CLI installation and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Dgate MCP access or install or refresh the Dgate CLI, then verify connectivity and identity before using downstream Dgate tools.

### Deployment Geography for Use:

Global, with the Dgate endpoint and AccessToken matched to the selected Alibaba Cloud region.

## Known Risks and Mitigations:

Risk: Dgate AccessTokens or install tokens could be exposed if pasted into chat, logs, URLs, source files, screenshots, or artifacts.

Mitigation: Keep tokens in encrypted agent configuration or environment variables and avoid printing, storing, or transmitting token values in plaintext.

Risk: MCP configuration changes or installer execution can alter the user's agent environment.

Mitigation: Require explicit user approval before modifying MCP settings or running downloaded installer commands, and preserve unrelated configuration.

Risk: A mismatched Dgate endpoint region and AccessToken region can cause failed or unintended access attempts.

Mitigation: Use a Region-matched Dgate token and endpoint, then verify the connection, discovered tool list, and identity before reporting success.

Risk: Overbroad Dgate instance authorization could expose resources beyond the intended setup workflow.

Mitigation: Use least-privilege Dgate instance authorization and rely on Dgate ACL, security policy, and audit controls for downstream operations.

## Reference(s):

- [RAM permissions](references/ram-policies.md)
- [Dgate CLI installation guide](https://d.tb.cn/install_cli.md)
- [ClawHub skill release page](https://clawhub.ai/sdk-team/skills/alibabacloud-aidbs-dgate-skill)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, markdown]

**Output Format:** [Markdown with JSON, bash, and PowerShell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before changing MCP configuration or running installer commands; secrets should remain in encrypted configuration or environment variables.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
