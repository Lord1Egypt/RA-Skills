## Description:

Provides advisory routes and a next step for customer website tasks and blocked or failing web requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agent-help-network](https://clawhub.ai/user/agent-help-network)

### License/Terms of Use:

MIT-0

## Use Case:

Agents handling customer website tasks or diagnosing blocked or failing web steps use the skill to check declared agent policies, official paths, provider status, and recent reports before choosing a next action. Its records are advisory, not guarantees or advice; platform rules and user instructions take precedence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional submission features can send observations, feedback, or task-route reports remotely.

Mitigation: Use submission features only with explicit user approval, and review each submission before approving it.

Risk: The scan was partial because several local path-like references could not be matched, so the evidence is incomplete.

Mitigation: Review the available source and scan results before installation, including unresolved local references.

## Reference(s):

- [Agent Help Network](https://agenthelpnetwork.com)
- [Agent instructions](https://agenthelpnetwork.com/agent-instructions.txt)
- [API schema](https://agenthelpnetwork.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise advisory response with task routes or incident status and one next action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records are advisory and do not guarantee a route or site availability.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
