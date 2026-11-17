## Description:

Establishes project-agnostic collaboration control for multi-agent work by defining authority, transition journals, evidence gates, active support watches, and handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to keep consequential multi-agent projects under explicit human authority, assign one writer per mutable surface, record evidence-bearing transitions, and manage handoffs or recurring support watches. It is useful for long-running research campaigns, live experiments, production automation, incident recovery, and consequential artifact work where claim promotion and operational state must stay distinct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the protocol or validator as an authorization system, sandbox, scheduler, lock, or proof that evidence is true.

Mitigation: Bind real project authority, access controls, journal paths, evidence requirements, and human escalation before live mutation; treat the validator as a schema helper only.

Risk: Ongoing support watches can create operational risk if targets, cadence, cost, state paths, stop conditions, or escalation authority are vague.

Mitigation: Pin trusted versions and define exact targets, read-only side-effect limits, budget, cadence, durable state, report destination, stop rules, and renewal conditions before claiming active support.

Risk: A stale handoff, terminal pane, process ID, heartbeat, or utilization sample can be mistaken for current authority or healthy progress.

Mitigation: Re-measure current state before mutation, require workload-specific monotonic progress evidence, supersede old events instead of editing them, and escalate unresolved ambiguity to the named human authority.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/agent-collaboration-control)
- [README](README.md)
- [Skill Protocol](SKILL.md)
- [Collaboration Framework Template](assets/COLLABORATION_FRAMEWORK.template.md)
- [Example Collaboration Policy](assets/collaboration-policy.example.json)
- [Example Transition Event](assets/transition-event.example.json)
- [Transition Event Validator](scripts/validate_transition_event.py)
- [Agent Orchestra](https://github.com/AntreasAntoniou/agent-orchestra)
- [Plus Ultra](https://github.com/AntreasAntoniou/plus-ultra)
- [Grade-A Pipeline](https://github.com/AntreasAntoniou/grade-a-pipeline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, JSON, Shell commands]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-specific collaboration contracts, transition events, receipts, advisories, and handoff summaries; the local validator emits PASS or structured error text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
