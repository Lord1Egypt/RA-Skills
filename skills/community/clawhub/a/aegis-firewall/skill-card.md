## Description:

Aegis Firewall provides dual-mode defensive review guidance for prompt-injection containment, pre-execution risk review, background anomaly detection, and security review of commands, scripts, installers, artifacts, patches, diffs, or repository behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alethean-kaw](https://clawhub.ai/user/alethean-kaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add structured caution when handling untrusted content, risky commands, installers, artifacts, diffs, and security claims. It helps separate reading from execution and produces evidence-backed review outcomes before higher-risk actions proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-risk actions such as network installs, secret access, destructive commands, or persistence changes may be delayed by confirmation requirements.

Mitigation: Provide explicit intent for high-risk actions and prefer static inspection or redacted evidence before execution.

Risk: Lightweight review can surface suspicious patterns without proving a complete attack path.

Mitigation: Treat findings as evidence-backed guidance and escalate to a full repository security scan when broader assurance is needed.

## Reference(s):

- [Detection Checklist](references/detection-checklist.md)
- [Examples And Test Samples](references/examples.md)
- [Review Output](references/review-output.md)
- [ClawHub Skill Page](https://clawhub.ai/alethean-kaw/skills/aegis-firewall)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured conversational Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces No findings, Security finding, or Blocked proof gap outputs by default; full scan artifacts are only used after explicit escalation.]

## Skill Version(s):

3.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
