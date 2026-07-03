## Description: <br>
Weekly strategy evolution insights from APEX's self-improvement engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to request weekly APEX Runner strategy evolution signals, review strategy changes, and calibrate long-term trading alignment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an agent to access a raw EVM private key for paid x402 requests. <br>
Mitigation: Use a dedicated low-balance wallet on Base and avoid reusing personal or treasury wallet keys. <br>
Risk: Automatic x402 requests can incur per-call charges of about $15 before discounts. <br>
Mitigation: Require explicit confirmation before each request and monitor wallet call history and balance. <br>


## Reference(s): <br>
- [APEX Evolution Insight endpoint](https://apexrunner.ai/signals/apex-evolution-insight) <br>
- [APEX pricing tier lookup](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner](https://apexrunner.ai) <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/apex-evolution-insight) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Code, Guidance] <br>
**Output Format:** [Markdown guidance with a Python example and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and USDC on Base mainnet for x402-authenticated paid requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
