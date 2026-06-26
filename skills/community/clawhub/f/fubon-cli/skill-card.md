## Description: <br>
AI-agent skill for Taiwan stock, futures, and options operations via fubon-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mofesto](https://clawhub.ai/user/Mofesto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading operators use this skill to run Fubon Neo authentication, account queries, market data retrieval, realtime subscriptions, conditional orders, and order lifecycle workflows through fubon-cli. It is intended to produce parseable command output and execution guidance for downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live brokerage orders, cancellations, modifications, conditional orders, and retries. <br>
Mitigation: Require explicit human confirmation for each trading action and verify symbol, quantity, price, account index, and resulting order state. <br>
Risk: Credentials, certificate paths, certificate passwords, and API keys are required for Fubon Neo workflows. <br>
Mitigation: Keep secrets out of chat and logs, avoid echoing raw credentials, and use secure local secret handling before running commands. <br>
Risk: The workflow depends on installing fubon-cli and a platform wheel for fubon_neo. <br>
Mitigation: Verify package and wheel sources before installation and start with read-only quote or account-query commands before enabling order actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or JSONL command output contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-streaming commands return success/data or success/error JSON objects; streaming commands emit JSONL.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
