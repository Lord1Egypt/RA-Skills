## Description:

Daily low-token, safety-first upskilling loop for OpenClaw multi-agent teams. Runs configurable micro-drills, scores quality, and produces a compact daily digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musashi94](https://clawhub.ai/user/musashi94)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use AgentDojo to run recurring, bounded micro-drills for OpenClaw agent teams, score the results, and produce compact daily improvement digests. It is intended for controlled upskilling loops where source quality, cost, and safety limits must be enforced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring drills may run with unsuitable schedule, timezone, budget, selected-agent, or local record paths for a given workspace.

Mitigation: Review and adjust the daily schedule, Europe/Berlin timezone default, USD and token budgets, selected agents, and report/state/audit paths before installation.

Risk: Open-web learning can expose the agent to low-quality sources or prompt-injection attempts.

Mitigation: Keep guarded web-source handling enabled, enforce the configured source score threshold, ignore policy override attempts from fetched content, and quarantine suspicious runs.

Risk: Unbounded learning loops could waste tokens, cost, or tool calls.

Mitigation: Use the configured hard caps for max daily tokens, max run tokens, max runs per agent per day, max team runs, tool calls, fetches, writes, and runtime.

## Reference(s):

- [AgentDojo README](artifact/README.md)
- [Architecture](artifact/docs/architecture.md)
- [Threat Model](artifact/docs/threat-model.md)
- [Scoring Rubric](artifact/docs/scoring-rubric.md)
- [AgentDojo ClawHub Page](https://clawhub.ai/musashi94/skills/agentdojo)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Compact Markdown daily digest, run record JSON, audit events, and configuration-guided recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default configuration uses isolated sessions, guarded web sources, hard tool limits, token budgets, and compact reporting.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
