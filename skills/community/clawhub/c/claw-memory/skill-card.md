## Description:

Claw Memory helps agents store, retrieve, search, and share memories across agent instances through a remote shared-memory service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siddontang](https://clawhub.ai/user/siddontang)

### License/Terms of Use:


## Use Case:

External developers and agent users use this skill to set up a shared memory space, store and search memories, and import existing memory files for reuse across agent instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive memory content may be persistently uploaded to a third-party remote service.

Mitigation: Review and redact selected memories before upload, and avoid sending private or regulated content unless the service has been approved for that use.

Risk: Bulk importing MEMORY.md can expose more historical agent context than intended.

Mitigation: Inspect MEMORY.md first, remove secrets and unnecessary personal or project data, and import only the entries that need to be shared.

Risk: Bearer tokens and encryption keys can expose or lock access to stored memories if mishandled.

Mitigation: Keep tokens and encryption keys private, do not reuse the encryption key elsewhere, and store credentials only in approved secret storage.

Risk: A mutable main-branch curl install can change the installed skill without prior review.

Mitigation: Install from a pinned and verified source when possible, then review and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siddontang/skills/claw-memory)
- [Claw Memory service API](https://claw-memory.siddontang.workers.dev)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands that create tokens and send selected memory content to a remote third-party service.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
