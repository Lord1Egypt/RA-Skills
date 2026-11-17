## Description:

Manage Flux kanban boards, cards, columns, and labels through the Flux REST API. Create and move cards, assign members, toggle labels, search, and build board automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uminai-dev](https://clawhub.ai/user/uminai-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent manage Flux workspaces, boards, columns, cards, labels, comments, attachments, search, and undo workflows through the Flux REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through write operations that create, move, assign, comment on, or delete Flux boards and cards.

Mitigation: Use a Flux API key with the narrowest scopes needed and review proposed write operations before approval, especially in shared workspaces.

Risk: Retries of write requests can duplicate board or card changes if idempotency is omitted.

Mitigation: Include an X-Idempotency-Key value on POST, PATCH, PUT, and DELETE requests as described by the artifact.

## Reference(s):

- [Flux](https://flux.umin.ai)
- [Flux API reference](https://flux.umin.ai/llms.txt)
- [Flux interactive API docs](https://flux.umin.ai/api-docs)
- [ClawHub Flux Board skill page](https://clawhub.ai/uminai-dev/skills/flux-kanban-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with REST API paths, JSON request examples, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Flux API key supplied through FLUX_API_KEY; FLUX_BASE_URL is optional.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
