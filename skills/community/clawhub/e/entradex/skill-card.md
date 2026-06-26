## Description: <br>
Use the EntradeX CLI for DNSE workflows. Use when (1) setting DNSE API credentials via env vars or config file, (2) reading account, market, and order data, (3) placing, modifying, or canceling real trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hieuhani](https://clawhub.ai/user/hieuhani) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading operators use this skill to configure EntradeX credentials, inspect DNSE account and market data, and prepare or run EntradeX CLI commands for DNSE order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable live DNSE order placement, modification, or cancellation using supplied credentials. <br>
Mitigation: Require explicit approval before every live trading action and prefer a limited-permission or separate trading account. <br>
Risk: DNSE_API_KEY and DNSE_API_SECRET are sensitive trading credentials. <br>
Mitigation: Keep credentials out of chat and logs, store them only in the intended config or environment, and rotate keys if exposure is suspected. <br>
Risk: Installing the wrong package could delegate trading access to untrusted code. <br>
Mitigation: Verify the entradex-cli npm package and publisher before installation. <br>


## Reference(s): <br>
- [EntradeX CLI npm package](https://www.npmjs.com/package/entradex-cli) <br>
- [DNSE OpenAPI endpoint](https://openapi.dnse.com.vn) <br>
- [ClawHub skill page](https://clawhub.ai/hieuhani/entradex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live trading commands that require explicit user approval before execution.] <br>

## Skill Version(s): <br>
0.1.16 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
