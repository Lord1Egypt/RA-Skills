## Description:

Uses the Tavily Search API to run web search and lightweight research for recent information, current events, online sources, or topic research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxindavid](https://clawhub.ai/user/liuxindavid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent Tavily-backed web and news search without installing the Tavily Python SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted search query could become shell command execution if the command template is followed literally.

Mitigation: Invoke the script through an argument-array or subprocess path where the query is passed as one argument, and do not interpolate the query into a shell command.

Risk: Tavily API keys can be exposed through command-line arguments or weak secret-file handling.

Mitigation: Prefer TAVILY_API_KEY or a protected .secrets/tavily.key file, and keep the secret file readable only by the user or service that runs the skill.

Risk: Search queries are sent to Tavily.

Mitigation: Avoid submitting sensitive, confidential, or regulated information in search queries unless that disclosure is approved for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuxindavid/skills/cliby-tavily-search)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Human-readable search results or raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include answer summaries, ranked result links, snippets, image URLs, response time, and Tavily credit usage.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
