## Description:

Guides an agent through Aicoo group chat workflows, including creating groups, sending messages, inviting members, managing settings, listing groups, leaving groups, and generating join links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate authenticated Aicoo group chat workflows through documented API calls and management endpoints. It is intended for creating coordination groups, broadcasting updates, inviting collaborators, reading group activity, and changing group settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad group messaging and group-management actions through authenticated Aicoo endpoints.

Mitigation: Require explicit user confirmation before sending messages, creating invite links, inviting or removing members, changing settings, or using contacts and network data to identify people.

Risk: Search and retrieval across conversations can expose group content beyond the user's immediate request.

Mitigation: Scope searches to the requested group or conversation view and confirm before searching outside group conversations.

Risk: Session-authenticated management endpoints can change membership, settings, and join-link availability.

Mitigation: Use least-privileged authenticated sessions and restrict administrative actions to users with verified group-admin intent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xisen-w/skills/aicoo-group-chat)
- [Aicoo unified message API](https://www.aicoo.io/api/v1/agent/message)
- [Aicoo conversations API](https://www.aicoo.io/api/v1/conversations?view=group)
- [Aicoo groups API](https://www.aicoo.io/api/groups)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated Aicoo API key or session token depending on endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
