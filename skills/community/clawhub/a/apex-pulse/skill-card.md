## Description: <br>
APEX system heartbeat — confirms live trading is active and healthy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Apex Pulse to check whether APEX Runner's live autonomous crypto trading system is active and fresh before relying on related signals or trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC from the configured EVM wallet each time an agent calls the paid endpoint. <br>
Mitigation: Use a dedicated low-balance Base wallet, confirm the price before use, and gate repeated or automated calls. <br>


## Reference(s): <br>
- [Apex Pulse signal endpoint](https://apexrunner.ai/signals/apex-pulse) <br>
- [Apex Pulse pricing](https://apexrunner.ai/signals/my-pricing) <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/apex-pulse) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with Python example and JSON response payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402 payment; the endpoint charges USDC per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
