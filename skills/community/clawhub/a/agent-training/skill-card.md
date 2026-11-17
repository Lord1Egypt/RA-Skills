## Description:

Agent Training System helps a main agent train and supervise multi-agent teams by maintaining training manuals, onboarding sub-agents, aligning responsibilities, and checking agent status and evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlim5](https://clawhub.ai/user/zlim5)

### License/Terms of Use:


## Use Case:

Developers and operators managing multiple agent roles use this skill to create training manuals, onboard sub-agents, and review whether the agent team remains consistent and up to date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent user profile and memory files may expose sensitive personal context across agents.

Mitigation: Review every USER.md and MEMORY.md copy or update, keep sensitive facts out of shared agent memory, and provide a process to inspect, edit, expire, or delete stored memories.

## Reference(s):

- [Agent training manual template](references/training-manual-template.md)
- [ClawHub skill page](https://clawhub.ai/zlim5/skills/agent-training)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown templates, checklists, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update persistent per-agent profile and memory files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
