## Description:

Shared semantic memory store for AI agents. Store, search, and retrieve memories across agents with TTL decay. SQLite persistence; survives restarts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kgnvsk](https://clawhub.ai/user/kgnvsk)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to run a local memory service that stores, searches, retrieves, and deletes agent memories with TTL-based expiry and SQLite persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private memory data can be exposed through an unauthenticated network service.

Mitigation: Run only on a trusted, isolated host unless authentication, loopback binding, owner-level authorization, and request limits are added.

Risk: Memory text can be sent to OpenAI for embeddings when OPENAI_API_KEY is configured.

Mitigation: Require clear opt-in before enabling OpenAI embeddings and avoid storing secrets or sensitive user data.

Risk: Persistent memory can retain sensitive agent data beyond a single session.

Mitigation: Add deletion controls and retention practices before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kgnvsk/skills/agent-memory-store)
- [Skill homepage](https://kgnvsk.github.io/paylock)
- [OpenAI embeddings API](https://api.openai.com/v1/embeddings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown instructions with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a local HTTP service on port 8768, persists data in SQLite, and can use OpenAI embeddings when OPENAI_API_KEY is configured.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
