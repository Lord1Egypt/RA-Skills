## Description:

Create, inspect, update, illustrate, export, and share live Coret mind maps through Coret MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramaaditya49](https://clawhub.ai/user/ramaaditya49)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill to create or update Coret mind maps from notes, meetings, research, plans, or outlines, and to inspect, export, or share existing maps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can read or change live Coret mind maps through the connected Coret MCP workspace.

Mitigation: Confirm the target workspace before live writes and use a test API key when trying new workflows.

Risk: Deletion, destructive batch updates, or public share links can remove or expose map content.

Mitigation: Review affected branches, require explicit confirmation for deletions, and create public links only when requested with clear permission and expiry.

Risk: CORET_API_KEY exposure could grant unwanted access.

Mitigation: Never print, store, commit, place the API key in URLs, prompts, maps, logs, or share links.

## Reference(s):

- [Coret Mind Map Skill Page](https://clawhub.ai/ramaaditya49/skills/coret-mindmap)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, API Calls, Guidance]

**Output Format:** [Agent guidance and Coret MCP tool calls, with optional JSON, Markdown, or text exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update live Coret mind maps, drawings, sketches, images, exports, and share links when requested.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
