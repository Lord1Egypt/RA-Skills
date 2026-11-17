## Description:

Routes tasks to the best-suited named agent based on skills, availability, cost tier, task priority, and dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to produce human-readable dispatch plans for multi-agent task queues, including suggested agent assignments, dependency phases, estimated cost, and warnings for unassigned work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the generated dispatch plan actually launches or manages agents.

Mitigation: Treat the output as a planning aid unless it is separately integrated with an execution system.

Risk: The fixed named roster, model labels, Korean display names, and cost tiers may not match a user's actual workflow or pricing.

Mitigation: Review and adjust the roster, labels, and cost assumptions before using plans for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/aoineco-squad-dispatch)
- [Publisher profile](https://clawhub.ai/user/edmonddantesj)

## Skill Output:

**Output Type(s):** [text, markdown, code]

**Output Format:** [Markdown-formatted dispatch plan text and Python data objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes named agent assignments, parallel or sequential phase grouping, estimated cost, estimated time, roster status, and warnings when no suitable agent is available.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
