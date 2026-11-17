## Description:

Commit agent context to DarkMatter, pull verified context from upstream agents, replay decision chains, fork from checkpoints, and verify chain integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bengunvl](https://clawhub.ai/user/bengunvl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to share, inherit, replay, fork, verify, and export agent execution context across multi-agent workflows with lineage tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected agent inputs, outputs, memory, and execution context to DarkMatter or a self-hosted DarkMatter instance.

Mitigation: Redact secrets, credentials, private prompts, regulated data, and unrelated conversation history before committing context.

Risk: Pulled, replayed, or inherited context may contain untrusted or unintended payloads.

Mitigation: Verify the sender, chain integrity, and intended use before relying on remote context or replayed payloads.

## Reference(s):

- [ClawHub Darkmatter Skill](https://clawhub.ai/bengunvl/skills/darkmatter)
- [DarkMatter Homepage](https://darkmatterhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the DARKMATTER_API_KEY environment variable.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
