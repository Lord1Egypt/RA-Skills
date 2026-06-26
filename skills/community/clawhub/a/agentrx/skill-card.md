## Description: <br>
AgentRx diagnoses AI agent tool failures, returns suggested recovery actions for agent evaluation, and provides preflight checks before risky tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chainassetslab](https://clawhub.ai/user/chainassetslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AgentRx to classify failed or risky external tool calls, receive recovery suggestions, and decide whether to retry, correct payloads, pause, or escalate to a human. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected tool-failure context and preflight payloads may be sent to the AgentRx third-party API. <br>
Mitigation: Redact secrets, credentials, regulated data, payment details, private prompts, and sensitive tool arguments before invoking AgentRx. <br>
Risk: Remote recovery suggestions may be wrong, out of scope, or risky for the current task. <br>
Mitigation: Treat every suggestion as advisory; evaluate it against the task, stop for human handoff or low confidence, and require human confirmation before writes, external communications, or data transfers. <br>
Risk: A shared beta key or incorrect service endpoint can weaken production controls. <br>
Mitigation: Use a dedicated API key, verify the base URL, avoid shared beta credentials for production, and rotate and monitor keys regularly. <br>


## Reference(s): <br>
- [AgentRx ClawHub page](https://clawhub.ai/chainassetslab/agentrx) <br>
- [Chain Assets homepage](https://chainassetslab.com) <br>
- [AgentRx API documentation](https://agentrx-production.up.railway.app/docs) <br>
- [AgentRx SDK on PyPI](https://pypi.org/project/agentrx-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON service responses with plaintext recovery guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTRX_API_KEY, AGENTRX_BASE_URL, curl, and jq; suggestions are advisory and require agent evaluation before action.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
