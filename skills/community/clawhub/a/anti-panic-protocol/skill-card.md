## Description:

Handle tool failures under pressure with bounded retries, clean user communication, and safe escalation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noelistired](https://clawhub.ai/user/noelistired)

### License/Terms of Use:


## Use Case:

Agents use this skill to handle command or tool failures with two bounded fix attempts, clear user-facing status, and explicit escalation when completion cannot be verified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Failure handling may use a Dutch escalation template that is not appropriate for every user or deployment audience.

Mitigation: Review and localize the escalation wording before deployment when the target audience does not use Dutch.

Risk: Repeated retries can create duplicate external sends, rate-limit pressure, or noisy user communication.

Mitigation: Keep retries bounded to two attempts, respect cooldowns, and escalate instead of looping.

Risk: An agent may claim completion before the failed action is actually resolved.

Mitigation: Verify the outcome before saying the task is done; report pending or failed status when verification is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noelistired/skills/anti-panic-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with short status and escalation messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bounded retry guidance, user-facing failure summaries, and escalation next steps.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
