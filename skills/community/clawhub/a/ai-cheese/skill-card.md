## Description: <br>
Send paid messages to real humans via the A.I. Cheese platform (aicheese.app) when an agent needs human input for surveys, feedback, photo tasks, local knowledge, or verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[locjonz](https://clawhub.ai/user/locjonz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search for human respondents, send paid USDC-backed messages, poll for replies, and register webhooks for human-in-the-loop tasks such as surveys, feedback, photo requests, local knowledge, and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real USDC from a raw wallet key without built-in spending caps or per-payment approval. <br>
Mitigation: Use a dedicated low-balance wallet, keep AGENT_PRIVATE_KEY out of logs and shared shells, and manually review each send before execution. <br>
Risk: Messages and replies pass through a third-party messaging service. <br>
Mitigation: Avoid sending secrets, regulated data, or sensitive business information through the service. <br>


## Reference(s): <br>
- [A.I. Cheese skill page](https://clawhub.ai/locjonz/ai-cheese) <br>
- [A.I. Cheese API base](https://aicheese.app) <br>
- [Base mainnet RPC endpoint](https://mainnet.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Console text and JSON-like API responses from CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx, a funded Base USDC wallet private key, and optional agent and webhook configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
