## Description:

Agent Causal Decision Tool returns structured JSON decisions, key statistics, and audit trails that help agents decide whether to ship, continue, reject, or escalate experiment changes across A/B tests, Bayesian A/B tests, Difference-in-Differences, cohort analysis, planning, and sequential early stopping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhumorris](https://clawhub.ai/user/zhumorris)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, product analysts, and AI agents use this skill to evaluate experiment or rollout summaries and produce defensible ship, continue, reject, targeted rollout, or review decisions with statistics and audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can fetch remote code, and the security evidence flags the mutable git clone install path as a review concern.

Mitigation: Prefer a pinned, checksummed release or isolated environment and avoid the mutable git clone install path.

Risk: HTTP JSON-RPC mode can expose a network-facing service if bound or routed beyond local development use.

Mitigation: Keep HTTP mode on localhost unless independent authentication and transport controls are added.

Risk: The PostHog connector makes outbound HTTPS requests and uses API credentials when explicitly invoked.

Mitigation: Use read-only PostHog tokens with minimal scopes and keep credentials in environment variables or local config rather than prompts or logs.

Risk: Experiment recommendations can be misleading when inputs are underpowered, aggregate-only, or violate method assumptions.

Mitigation: Review emitted warnings, confidence, limitations, and audit records before acting on ship, reject, or targeted rollout recommendations.

## Reference(s):

- [Agent Causal source repository](https://github.com/ZhuMorris/agent-causal-decision-tool)
- [Agent Causal ClawHub skill page](https://clawhub.ai/zhumorris/skills/agent-causal)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON decision objects, text summaries, and Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local SQLite audit and experiment history records when save or history commands are used.]

## Skill Version(s):

0.10.3 (source: artifact/_meta.json, SKILL.md metadata.openclaw.version, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
