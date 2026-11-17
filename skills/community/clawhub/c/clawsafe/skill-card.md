## Description:

Multi-layer security detector for AI agents that scans incoming text and code-like input for prompt injection, jailbreaks, XSS, SQL injection, API key leaks, supply chain patterns, and deployment vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silvertime](https://clawhub.ai/user/silvertime)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use ClawSafe as an input hook or middleware detector to screen agent-bound messages and code snippets before they reach an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security review flags the release as suspicious because default bypass rules and broken regex handling can let attacks pass despite the advertised protection.

Mitigation: Review the defaults before installation, remove or lock down the content-based whitelist, and fix invalid web rules before relying on the detector.

Risk: The hook runs on incoming messages and may log blocked attempts, which can expose sensitive message content depending on deployment logging.

Mitigation: Confirm how the OpenClaw deployment stores hook logs, restrict log access, and avoid retaining sensitive blocked inputs longer than necessary.

Risk: The detector is a content scanner and should not be treated as the only security boundary.

Mitigation: Use it as one layer alongside model-side safeguards, application authorization, input validation, secret handling controls, and human review for high-risk workflows.

## Reference(s):

- [ClawSafe on ClawHub](https://clawhub.ai/silvertime/skills/clawsafe)
- [Publisher profile](https://clawhub.ai/user/silvertime)
- [Repository listed in artifact metadata](https://github.com/openclaw/clawSafe)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JSON scan results and localized block messages, with Markdown documentation and JavaScript configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports safe status, detected threats, severity, confidence, and scanned layers.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
