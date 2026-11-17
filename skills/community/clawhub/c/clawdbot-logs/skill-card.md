## Description:

Analyze Clawdbot logs and diagnostics for bot performance, response times, errors, session stats, token usage, API costs, and slow-response debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satriapamudji](https://clawhub.ai/user/satriapamudji)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect local Clawdbot journal logs and session records when diagnosing performance, error patterns, response latency, token usage, and API cost behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect local Clawdbot logs and session records that may contain private conversation text or operational details.

Mitigation: Install only when the operator is trusted, scope commands to the needed session or time window, and redact sensitive output before sharing.

Risk: The raw recent-message command can expose private conversation content from session files.

Mitigation: Avoid raw message extraction unless explicitly needed, scoped to a chosen session, and reviewed for sensitive content before use.

Risk: The response-times script accepts a count argument that the security guidance says should be validated before use.

Mitigation: Use a small numeric count and validate or constrain the argument before running the script in shared or automated environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local diagnostics guidance and shell commands that inspect Clawdbot logs and session files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
