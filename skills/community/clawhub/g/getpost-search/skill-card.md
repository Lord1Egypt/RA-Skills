## Description:

Web search API for AI agents. Get search results with titles and snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dommholland](https://clawhub.ai/user/dommholland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add web search through the GetPost API and retrieve result titles, URLs, and snippets for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signup details and search queries are sent to getpost.dev.

Mitigation: Use only non-sensitive signup details and avoid submitting secrets or private data in search queries.

Risk: The skill requires a bearer API key for GetPost requests.

Mitigation: Store the API key securely and avoid exposing it in prompts, logs, shared files, or public transcripts.

Risk: Searches consume credits.

Mitigation: Set usage expectations before enabling the skill and monitor query volume.

## Reference(s):

- [GetPost Search API documentation](https://getpost.dev/docs/api-reference#search)
- [ClawHub skill page](https://clawhub.ai/dommholland/skills/getpost-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses include position, title, URL, and snippet; each search costs 3 credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
