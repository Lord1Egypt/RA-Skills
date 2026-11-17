## Description:

Use when you compost (or want to start) and the pile smells, stalls, or you don't know what to add: computes the C:N ratio of mixed ingredients from batch weights, diagnoses odor/moisture/temperature symptoms, fixes a pile with targeted 'add this much' prescriptions, sizes a system for your household waste stream, and tracks temperature curves. Solves the failed-backyard-pile problem that makes most beginners quit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External composters use the skill to diagnose backyard pile problems, calculate ingredient mixes and additions, size a household composting setup, and track pile temperatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The temperature logger's sanitation message could be mistaken for proof that compost is safe; it does not verify the required duration or turning.

Mitigation: Treat calculations as estimates and independently confirm sanitation time and turning conditions before relying on a safety conclusion.

## Reference(s):

- [Compost Engineering Reference](references/compost-engineering.md)
- [Compost Balancer on ClawHub](https://clawhub.ai/voronindenis5/skills/compost-balancer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Text recommendations and command-line output; optional JSON temperature log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temperature logging optionally writes compost_temp_log.json in the chosen working directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
