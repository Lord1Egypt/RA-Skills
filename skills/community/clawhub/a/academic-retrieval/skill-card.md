## Description:

Retrieves academic literature and patents through structured metadata search, semantic chunk retrieval, and character-range content reading for citation-grounded agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciverse](https://clawhub.ai/user/sciverse)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and researchers use this skill to find papers, authors, sources, and patents, retrieve relevant paper passages, and read source text for citation-grounded research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and filters are sent to Sciverse, and its retention practices were not verified.

Mitigation: Avoid confidential query terms unless sharing is intended; review Sciverse's current data-handling terms before sensitive use.

Risk: The API token authorizes requests to the Sciverse service.

Mitigation: Keep the token protected in the SCIVERSE_API_TOKEN environment variable and do not expose it in shared logs or prompts.

## Reference(s):

- [Sciverse service](https://sciverse.space)
- [ClawHub skill release](https://clawhub.ai/sciverse/skills/academic-retrieval)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown, Image data]

**Output Format:** [JSON search results, text and Markdown excerpts, and image data for referenced figures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may be paginated; full-text access depends on authorization.]

## Skill Version(s):

1.0.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
