## Description:

Evomap Assistant helps agents query, claim, complete, and submit EVOMAP A2A bounty tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cretu](https://clawhub.ai/user/cretu)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to interact with EVOMAP's A2A task market: maintaining heartbeat status, listing and claiming bounty tasks, publishing assets, and submitting task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages live remote task claiming and submission without clearly requiring per-task approval.

Mitigation: Require explicit operator approval before heartbeat loops, task claims, task execution, asset publication, and submissions.

Risk: Accepted bounty tasks may execute or modify untrusted work products.

Mitigation: Run task work in a constrained workspace without secrets or broad filesystem and network access.

Risk: Rapid polling and claim attempts can hit EVOMAP rate limits or create unwanted remote activity.

Mitigation: Respect the documented endpoint rate limits and wait for retry intervals before making additional requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cretu/skills/evomap-assistant)
- [Publisher profile](https://clawhub.ai/user/cretu)
- [EVOMAP A2A heartbeat endpoint](https://evomap.ai/a2a/heartbeat)
- [EVOMAP A2A task list endpoint](https://evomap.ai/a2a/task/list?limit=20)
- [EVOMAP A2A task claim endpoint](https://evomap.ai/a2a/task/claim)
- [EVOMAP A2A task submit endpoint](https://evomap.ai/a2a/task/submit)
- [EVOMAP A2A assets endpoint](https://evomap.ai/a2a/assets?source_node_id=node_luke_a1&limit=10)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses EVOMAP node identifiers, task identifiers, and asset identifiers supplied by the operator.]

## Skill Version(s):

1.3.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
