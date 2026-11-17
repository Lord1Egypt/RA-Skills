## Description:

In-memory key-value store with TTL for AI agents. Set, get, delete, list, flush, and stats. Supports any JSON value, optional TTL per key, and prefix-based key listing. Like a lightweight Redis for agent pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Kvstore to run a local HTTP key-value service for transient agent state, caching, and data sharing with optional TTL expiration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service exposes unauthenticated read, write, list, delete, and full-flush operations over stored data.

Mitigation: Keep it bound to localhost, avoid sharing the port with untrusted users, processes, or containers, and treat /v1/flush as an admin-only destructive action.

Risk: Data written to the store can include arbitrary JSON values that may be sensitive if callers choose to store secrets or personal data.

Mitigation: Do not store real secrets or sensitive personal data in this local service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/gh-kvstore)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for starting and calling a local FastAPI key-value service; stored values are JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
