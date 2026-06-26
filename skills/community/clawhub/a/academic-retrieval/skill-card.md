## Description: <br>
Retrieve academic papers by structured metadata, perform semantic chunk search for RAG, and read byte-range content for citation-grade scientific literature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciverse](https://clawhub.ai/user/sciverse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research agents use this skill to find academic papers, retrieve citation-grade snippets, inspect paper relationship lists, and fetch paper figure or table resources through Sciverse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Sciverse API token and sends search queries, document IDs, retrieval parameters, and requested resource names to Sciverse. <br>
Mitigation: Configure the token through environment management, scope access where the service supports it, and avoid sensitive research topics unless Sciverse account, logging, and data-handling terms are acceptable. <br>
Risk: Retrieved snippets, abstracts, relationship lists, and resource names may be incomplete or require additional context before citation use. <br>
Mitigation: Use schema introspection, structured search metadata, and byte-range expansion to verify the surrounding context before relying on excerpts or citations. <br>


## Reference(s): <br>
- [Sciverse](https://sciverse.space) <br>
- [ClawHub skill page](https://clawhub.ai/sciverse/skills/academic-retrieval) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, shell commands] <br>
**Output Format:** [JSON API responses, Markdown text excerpts, base64-encoded image resources, and shell invocation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCIVERSE_API_TOKEN; SCIVERSE_BASE_URL is optional and defaults to the Sciverse API.] <br>

## Skill Version(s): <br>
0.8.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
