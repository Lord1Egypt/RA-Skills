## Description:

Recall and store persistent memories in the user's brain (~/.brain) with the brain CLI: deterministic recall with spreading activation, spaced reinforcement after presenting results, and classified model-driven memorization across life domains (personal, family, social, professional).

This skill is ready for commercial/non-commercial use.

## Publisher:

[onurkarali](https://clawhub.ai/user/onurkarali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Brain Memory to let agents recall, reinforce, and store durable user memories across sessions via the brain CLI. It is suited for workflows where persistent context is intentionally shared across agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may expose sensitive user data across sessions or agents.

Mitigation: Install only when shared persistent memory is intentional, treat recalled and stored memories as sensitive data, avoid secrets and regulated information, and review stored memories regularly.

Risk: The memory store is global by default under ~/.brain, which can blur boundaries between projects or agents.

Mitigation: Isolate ~/.brain per project or agent when separation matters.

Risk: The install evidence references an unpinned brain-memory executable package.

Mitigation: Prefer a pinned and audited brain-memory package before deployment.

## Reference(s):

- [Brain Memory homepage](https://brainmemory.ai)
- [ClawHub skill page](https://clawhub.ai/onurkarali/skills/brain-memory)
- [ClawHub publisher profile](https://clawhub.ai/user/onurkarali)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the brain CLI to recall, reinforce, and memorize entries; normal operation can read and write persistent memory under ~/.brain.]

## Skill Version(s):

0.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
