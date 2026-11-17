## Description:

Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regan-milne](https://clawhub.ai/user/regan-milne)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to save, load, and manage encrypted AI memory across sessions and machines through a remote Jackal-backed storage service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved memories depend on a long-term encryption key that could expose memory contents if logged, shared, or stored with broad file permissions.

Mitigation: Create the key file with owner-only permissions, avoid running keygen or first-run setup where output is logged, and never expose JACKAL_MEMORY_ENCRYPTION_KEY in chat or command logs.

Risk: The skill stores AI memory remotely and sends requests authenticated by JACKAL_MEMORY_API_KEY.

Mitigation: Install only if remote memory storage fits the deployment, keep the API key out of logs, and rotate or revoke the key if exposure is suspected.

Risk: The client requires an external cryptography dependency.

Mitigation: Install dependencies in an isolated environment with pinned versions before using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/regan-milne/skills/claw-store-skill)
- [Claw Store homepage](https://web-production-5cce7.up.railway.app)
- [Claw Store API key login](https://web-production-5cce7.up.railway.app/auth/login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JACKAL_MEMORY_API_KEY and uses a local or environment-provided encryption key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
