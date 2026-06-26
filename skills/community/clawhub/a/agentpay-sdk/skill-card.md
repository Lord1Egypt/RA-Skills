## Description: <br>
Install and operate the AgentPay SDK for wallet setup, funding checks, funding instructions or QR generation, policy changes, manual approvals, transfers, approvals, broadcasts, x402 payments, MPP payments, and supported plugin-backed merchant payment flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlfi-dev1](https://clawhub.ai/user/wlfi-dev1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and operate AgentPay workflows from an agent, including self-custodial wallet setup, funding guidance, policy configuration, manual approvals, crypto transfers, and paid API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install persistent payment tooling. <br>
Mitigation: Install only after trusting the publisher and inspecting or verifying the wlfi.sh installer. <br>
Risk: The skill can move crypto funds and authorize payments. <br>
Mitigation: Use a dedicated wallet with limited funds, spending limits, and manual approvals before authorizing payment actions. <br>
Risk: Sensitive wallet, backup, or plugin session material could be exposed in chat. <br>
Mitigation: Keep vault passwords, backup passwords, and plugin session material out of chat; use secure local prompts for wallet and admin flows. <br>
Risk: Under-scoped payment defaults can lead to unintended network, asset, recipient, spender, amount, or broadcast behavior. <br>
Mitigation: Explicitly confirm network, asset, recipient, spender, amount, broadcast flag, and any MPP amount cap before approving payments. <br>


## Reference(s): <br>
- [AgentPay SDK ClawHub page](https://clawhub.ai/wlfi-dev1/agentpay-sdk) <br>
- [Publisher profile](https://clawhub.ai/user/wlfi-dev1) <br>
- [World Liberty Financial](https://worldlibertyfinancial.com) <br>
- [Capabilities](references/capabilities.md) <br>
- [Install And Workflows](references/install-and-workflows.md) <br>
- [Intents And Policies](references/intents-and-policies.md) <br>
- [MPP Services](references/mpp-services.md) <br>
- [MPP service directory](https://mpp.dev/services/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON funding payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include funding addresses, network details, funding URIs, QR images or QR URLs, and local CLI approval steps.] <br>

## Skill Version(s): <br>
0.3.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
