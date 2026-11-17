## Description:

A structured 7-phase workflow for collaborative human and AI debugging of complex, intermittent, multi-layered, or cross-system bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure difficult debugging sessions where symptoms are intermittent, contradictory, long-running, or span multiple services and systems. It guides the agent and user through flow alignment, symptom structuring, boundary probing, solution selection, verification, escalation, and documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent toward broad debugging and fix actions in live systems.

Mitigation: Require explicit approval before Kubernetes, SSH, database, network, restart, configuration, data-changing, or documentation-writing actions.

Risk: The skill may operate with sensitive infrastructure or production context during debugging.

Mitigation: Use read-only credentials where possible and grant only the narrow environment access needed for the investigation.

Risk: The artifact states a preferred model requirement that may not match the runtime environment.

Mitigation: Treat the model requirement as advisory and validate conclusions against observed data, code, logs, and user-confirmed facts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hgvgfgvh/skills/complex-bug-debugging-with-ai-en)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code]

**Output Format:** [Markdown guidance with checklists, diagrams, decision tables, and inline command or code examples when the debugging task requires them.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are evidence-led and gated by user confirmation before higher-impact actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
