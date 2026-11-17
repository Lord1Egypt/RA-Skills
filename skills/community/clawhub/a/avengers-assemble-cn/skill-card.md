## Description:

A Chinese-language Avengers-themed multi-agent coordinator that routes user tasks to six reusable child-agent sessions with round-robin dispatch, threat-level assessment, and sessionKey reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxinbest](https://clawhub.ai/user/chenxinbest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to coordinate complex Chinese-language tasks by delegating work to specialized child-agent roles and combining their results. It is most relevant when task decomposition, parallel delegation, and reusable child-agent sessions are desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill forces nearly all work into reusable spawned sessions and overrides normal agent workflow.

Mitigation: Review before installing, avoid secrets or sensitive project context unless copying that context into spawned sessions is acceptable, and consider changing delegation to be optional and user-approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenxinbest/skills/avengers-assemble-cn)
- [Publisher profile](https://clawhub.ai/user/chenxinbest)
- [Marvel Avengers homepage](https://marvel.com/avengers)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown text with delegated child-agent task results and optional code or command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on spawned child-agent sessions; the skill instructs a fixed 300 second run timeout for delegated tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
