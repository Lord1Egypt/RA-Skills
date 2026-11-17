## Description:

Get笔记 helps agents save, search, and manage personal notes and knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horisony](https://clawhub.ai/user/horisony)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to connect to Getnote, save text, link, and image notes, search private notes, and manage tags and knowledge-base membership through the Getnote OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private note content and perform remote account changes with under-scoped authorization and confirmation safeguards.

Mitigation: Install only after review, configure an owner identity, and use the least-privileged Getnote API scopes available.

Risk: The skill can delete notes, change tags or knowledge-base membership, follow live content, upload images, and create public share links.

Mitigation: Require clear user confirmation before any destructive, public-sharing, upload, subscription, or knowledge-base membership action.

Risk: The skill may expose private note content in shared agent, group chat, or workspace contexts.

Mitigation: Avoid displaying private note content in shared contexts unless the configured owner identity matches the requesting user.

## Reference(s):

- [Getnote homepage](https://biji.com)
- [Getnote OpenAPI base URL](https://openapi.biji.com)
- [Get笔记 API detailed reference](references/api-details.md)
- [Save notes reference](references/save.md)
- [Search reference](references/search.md)
- [Note list and detail reference](references/list.md)
- [Tag management reference](references/tags.md)
- [Knowledge-base management reference](references/knowledge.md)
- [Authorization configuration reference](references/oauth.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with API request examples and JSON handling rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Getnote credentials and may operate on private notes, tags, knowledge bases, uploads, and public share links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
