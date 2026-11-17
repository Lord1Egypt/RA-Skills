## Description:

Helps agents search the web, images, news, and videos through Brave Search using a Maton-managed connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can retrieve Brave Search results for web pages, images, news, and videos. A Maton account and authorized connection are required; optional automation requires separate user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and connection requests pass through Maton as a managed gateway.

Mitigation: Use only if comfortable with Maton handling the connection; approve new connections explicitly and keep access limited to the task.

Risk: Optional hosted functions, triggers, destinations, and event watching can automate data flow or run a local handler.

Mitigation: Approve automation only after reviewing the data, destination, handler, and deletion procedure; do not enable it for ordinary searches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/brave-search-api)
- [Maton homepage](https://maton.ai)
- [Brave Search API documentation](https://api-dashboard.search.brave.com/documentation)
- [Maton documentation](https://docs.maton.ai)
- [Maton API reference](https://docs.maton.ai/api-reference/overview)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with search results and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include links and snippets; the skill also describes optional Maton automation.]

## Skill Version(s):

1.2.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
