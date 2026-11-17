## Description:

Search the Andara Ionic RAG knowledge base (3,800+ records) for business intel, research, products, team, meetings, and any indexed content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atiati82](https://clawhub.ai/user/atiati82)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and authorized operators use this skill to search Andara Ionic business, meeting, product, customer, CMS, and research records through read-only PostgreSQL queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive business, customer, personnel, email, equity, order, and meeting data from the referenced Andara database.

Mitigation: Install only where users are authorized for that database and avoid returning sensitive fields unless the request is clearly authorized.

Risk: The documented shell SQL pattern can be unsafe if untrusted search text is pasted directly into a query.

Mitigation: Use a read-only, least-privilege DATABASE_URL and parameterize or otherwise safely quote search terms before execution.

Risk: Queries against broad base tables can return more information than the user needs.

Mitigation: Prefer approved views where available, keep default LIMIT values small, and truncate long content fields.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atiati82/skills/andara-rag-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline SQL and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses concise result limits and truncated content previews for database query results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
