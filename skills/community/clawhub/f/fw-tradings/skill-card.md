## Description: <br>
FW-trading routes an agent through Fosun Wealth Hong Kong and U.S. stock OpenAPI workflows for shared credential setup, account and market-data queries, holdings and cash checks, and confirmed real or simulated order changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fosunwealth](https://clawhub.ai/user/fosunwealth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to prepare Fosun Wealth OpenAPI credentials, choose real or simulated trading, inspect accounts, cash, holdings, orders, and market data, and submit order changes only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access live brokerage data and place live trades after confirmation. <br>
Mitigation: Install only from a trusted publisher, verify every real-trade intent before confirmation, and use simulated trading first for unfamiliar workflows. <br>
Risk: The skill handles API keys, public-key material, fosun.env, and local credential backups. <br>
Mitigation: Avoid pasting secrets into chat, restrict permissions on fosun.env and backup directories, and rotate or revoke credentials if exposure is suspected. <br>
Risk: The installer retrieves remote tools and SDK dependencies. <br>
Mitigation: Prefer manual dependency installation or review the installer and dependency sources before using the skill with real accounts. <br>


## Reference(s): <br>
- [FW-trading ClawHub release page](https://clawhub.ai/fosunwealth/fw-tradings) <br>
- [Credential management flow](artifact/fosun-env-setup/reference/credential-management-flow.md) <br>
- [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update fosun.env and local credential backups; credential setup can also generate QR image artifacts.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
