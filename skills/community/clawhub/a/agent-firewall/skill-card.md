## Description:

Agent Firewall provides real-time input and output filtering for agent communications to block prompt injection, data exfiltration, and unauthorized commands before they reach the model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arhadnane](https://clawhub.ai/user/arhadnane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use Agent Firewall to pre-filter agent inputs and outputs for prompt-injection patterns, sensitive-data exposure, PII, and risky content before messages continue through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive prompts, tokens, or metadata may be retained in plaintext logs.

Mitigation: Disable logging or rewrite it to redact and bound context before using the skill with sensitive data.

Risk: Consumers may accidentally use unfiltered originalData returned alongside processedData.

Mitigation: Integrate callers to consume processedData only and ignore originalData in downstream agent steps.

Risk: Advertised protections should not be treated as a dependable security boundary.

Mitigation: Use the skill as an advisory local filter until custom rules, rate limits, URL blocking, and command blocking are implemented and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arhadnane/skills/agent-firewall)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with processedData, actions, status, and error fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include original input or output text and filter actions; review logging behavior before use with sensitive data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
