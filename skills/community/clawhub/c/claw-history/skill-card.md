## Description:

Provide a chronological history of all actions the agent has taken from the beginning (birth) until now.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluebirdback](https://clawhub.ai/user/bluebirdback)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to reconstruct an auditable timeline of an agent's activity from available memories, session histories, command logs, and current conversation records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad persistent memories, session histories, sub-agent records, and command logs that can contain secrets, private paths, customer data, credentials, or unrelated work.

Mitigation: Review before installing in sensitive environments, use only where full local history access is acceptable, and define clear logging retention and deletion practices.

Risk: Timeline completeness depends on available memories, session histories, and command logs, so missing or inaccessible sources can lead to incomplete history.

Mitigation: Have the agent report unavailable sources, visible date ranges, gaps, and confidence, and enable the recommended session-memory and command-logger hooks when full auditing is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluebirdback/skills/claw-history)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown chronological timeline with source coverage, gaps, and confidence notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shell commands for optional OpenClaw hook setup when explaining recommended history sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
