## Description:

Prevents LLMs from sunk-cost pushing broken solutions. Triggers when an agent is stuck, looping, or failing repeatedly. Forces a Popperian falsification moment, then generates 3 constrained-chaotic alternative approaches and picks the best one. Loops like design thinking until solved or escalated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manecharo](https://clawhub.ai/user/manecharo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent stop repeating failed approaches, diagnose the failed assumption, generate three divergent alternatives, test for signal, and escalate after repeated unsuccessful loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger language may cause the skill to redirect an agent's workflow during ordinary uncertainty or longer tasks.

Mitigation: Use the skill when the agent is repeatedly stuck, looping, or failing, and review whether a pivot is warranted before abandoning the current approach.

## Reference(s):

- [Chaos Pivot on ClawHub](https://clawhub.ai/manecharo/skills/chaos-pivot)
- [Manecharo publisher profile](https://clawhub.ai/user/manecharo)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown or plain text reasoning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured dead-end declarations, alternative approaches, evaluation notes, audit verdicts, and escalation summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
