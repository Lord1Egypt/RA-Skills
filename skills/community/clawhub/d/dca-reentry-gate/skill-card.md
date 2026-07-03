## Description: <br>
DCA re-entry readiness gate based on F&G, RSI, Stoch, and SMA filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill before DCA entries to request a real-time readiness signal based on F&G, RSI, Stoch, and SMA filters. It is intended to help avoid re-entry during unfavorable market conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key to authorize paid x402 requests. <br>
Mitigation: Use only a dedicated low-balance wallet on Base, keep EVM_PRIVATE_KEY out of logs and shared prompts, and avoid wallets with funds beyond the intended signal budget. <br>
Risk: Automatic payment authorization can create unintended spend if calls are triggered without user control. <br>
Mitigation: Require deliberate confirmation before each paid call and monitor wallet call history and pricing tiers. <br>
Risk: Trading signals can be incorrect, stale, or unsuitable for a user's strategy. <br>
Mitigation: Treat the signal as decision support and review the returned status, reason, indicators, and timestamp before using it for DCA decisions. <br>


## Reference(s): <br>
- [DCA Re-entry Gate Signal](https://apexrunner.ai/signals/dca-reentry-gate) <br>
- [DCA Signal](https://apexrunner.ai/signals/dca-signal) <br>
- [Fear Greed Signal](https://apexrunner.ai/signals/fear-greed) <br>
- [Portfolio Heat Signal](https://apexrunner.ai/signals/portfolio-heat) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Guidance] <br>
**Output Format:** [Markdown with Python and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests using a wallet with USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
