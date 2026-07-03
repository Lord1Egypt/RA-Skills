## Description: <br>
Provides real-time BTC price ticks from live exchange feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill when they need a low-latency BTC price reference for polling loops, spread checks, or momentum calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an unrestricted EVM private key for automatic per-call payments, including possible polling loops. <br>
Mitigation: Use a dedicated low-balance wallet or delegated payment credential, and set external rate limits or spending controls before unattended use. <br>
Risk: Each request may spend funds because the BTC price feed is a paid x402-authenticated endpoint. <br>
Mitigation: Review pricing before use and monitor wallet call history and balance during operation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/btc-price-tick) <br>
- [APEX Runner BTC Price Tick](https://apexrunner.ai/signals/btc-price-tick) <br>
- [APEX Runner Pricing Tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner Market Tick](https://apexrunner.ai/signals/market-tick) <br>
- [APEX Runner Apex Pulse](https://apexrunner.ai/signals/apex-pulse) <br>
- [APEX Runner BTC Dominance](https://apexrunner.ai/signals/btc-dominance) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with endpoint details, Python example code, and JSON response example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
