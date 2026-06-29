## Description: <br>
Current Hyperliquid perpetual funding rates across tracked coins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and agents use this skill to retrieve live Hyperliquid perpetual funding rates before opening or holding positions, identifying funding arbitrage opportunities, or avoiding high funding costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC from a wallet through paid x402 requests. <br>
Mitigation: Use a dedicated low-balance wallet and require clear approval before the agent signs or sends any paid request. <br>
Risk: The EVM private key required by the skill could be exposed if placed in chats, logs, or shared configuration. <br>
Mitigation: Store the private key only in an environment variable or secret manager and keep it out of prompts, transcripts, and logs. <br>
Risk: Repeated calls can accumulate costs even when each request is low priced. <br>
Mitigation: Review the exact USDC amount before each request and set operational limits for agent-initiated calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/funding-rate-hl) <br>
- [APEX Runner funding-rate-hl signal](https://apexrunner.ai/signals/funding-rate-hl) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response data with agent-facing Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM private key and can trigger paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
