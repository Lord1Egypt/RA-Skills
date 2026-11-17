## Description:

Context Assembler is a dynamic context preprocessor for OpenClaw agents that selects relevant memory, collapses timelines, detects forbidden patterns, and injects task-specific context before agent reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wudi488](https://clawhub.ai/user/wudi488)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to assemble a compact, task-specific context block from local memory, recent notes, timeline signals, and repeated-failure patterns before an agent reasons over a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw memory files and may insert selected excerpts into an agent's prompt.

Mitigation: Review or redact sensitive memory before use and inspect the generated context block before allowing the agent to rely on it.

Risk: Task descriptions and selection metadata can be retained in the feedback log.

Mitigation: Disable, remove, or protect the feedback log when task descriptions may contain private or sensitive information.

Risk: Broad or generic invocation could add more local context than intended for a task.

Mitigation: Prefer explicit manual invocation with a clear task description and an appropriate token budget.

## Reference(s):

- [Context Assembler ClawHub listing](https://clawhub.ai/wudi488/skills/context-assembler)

## Skill Output:

**Output Type(s):** [text, guidance, configuration]

**Output Format:** [Plain text context block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-specific output is constrained by the token budget from genome.yml or the --max-tokens argument.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
