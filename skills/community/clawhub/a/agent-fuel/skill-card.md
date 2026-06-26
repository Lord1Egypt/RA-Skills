## Description: <br>
Autonomous agent wallet management with MoonPay auto top-up, x402 payments, and OpenWallet Standard. Agents never run out of gas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zedit42](https://clawhub.ai/user/Zedit42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Agent Fuel to monitor agent wallet balances, prepare MoonPay top-ups, and handle x402 payment flows with configurable spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic wallet top-ups and x402 payments can spend real funds beyond the operator's intent if defaults are trusted or limits are misconfigured. <br>
Mitigation: Use a dedicated low-limit wallet and funding source, disable daemon and x402 auto-pay by default, and require manual confirmation for buys and sends. <br>
Risk: The security review reports unsafe shell execution patterns and weak scoping for payment actions. <br>
Mitigation: Review commands before execution, validate recipients and 402 responses with allowlists, add cooldowns, and add a kill switch before deployment. <br>


## Reference(s): <br>
- [Agent Fuel release page](https://clawhub.ai/Zedit42/agent-fuel) <br>
- [x402 facilitator](https://x402.org/facilitator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute or recommend MoonPay CLI wallet actions when installed and configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
