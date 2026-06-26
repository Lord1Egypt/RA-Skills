## Description: <br>
Buy the latest machine-readable BTC directional signal from Crypto Engine through a Tempo MPP-enabled endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weifenghuang](https://clawhub.ai/user/weifenghuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to fetch Crypto Engine's live BTC directional signal when the runtime can complete a Tempo MPP payment challenge. It helps them return the API's direction, brief reason, and timestamp without inventing a fresh signal if payment or retrieval fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger a paid request for a BTC signal. <br>
Mitigation: Require an explicit user request, verify merchant identity, network, and amount before payment, and avoid subscriptions, prepayment, or repeated automatic purchases. <br>
Risk: The returned BTC direction could be mistaken for standalone financial advice. <br>
Mitigation: Present the direction with its brief reason and timestamp, and do not treat the signal as financial advice by itself. <br>
Risk: Payment handling could expose wallet secrets or unrelated credentials. <br>
Mitigation: Use runtime payment middleware, preserve required payment receipt headers, and never send wallet secrets, seed phrases, or unrelated credentials to the endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weifenghuang/crypto-engine-agent-signal) <br>
- [Crypto Engine discovery document](https://cryptoengine.club/api) <br>
- [Crypto Engine paid signal endpoint](https://cryptoengine.club/api/agent-signal) <br>
- [Crypto Engine public AI index](https://cryptoengine.club/llms.txt) <br>
- [Public skill instructions](https://cryptoengine.club/skills/crypto-engine-agent-signal/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, API Calls] <br>
**Output Format:** [JSON response fields plus concise text guidance when payment or retrieval cannot proceed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected response includes direction, brief_reason, and signal_timestamp; payment must be explicitly requested and completed before returning a live signal.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
