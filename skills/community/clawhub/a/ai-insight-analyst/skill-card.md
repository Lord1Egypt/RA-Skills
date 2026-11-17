## Description:

Helps AI practitioners search Jiqizhixin AI-industry insights, open detail records, and produce source-linked trend analysis, weekly reviews, topic retrospectives, and decision-support summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiqizhixin](https://clawhub.ai/user/jiqizhixin)

### License/Terms of Use:

MIT-0

## Use Case:

AI practitioners, analysts, and developers use this skill to retrieve Jiqizhixin insight summaries and full records, then synthesize source-linked AI industry trend analysis, weekly reviews, and topic deep dives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can send JQZX_API_TOKEN to an environment-controlled endpoint if BASE_URL is overridden.

Mitigation: Keep the default Jiqizhixin API host unless reviewed, avoid overriding BASE_URL, and prefer a version that pins or allowlists the API host.

Risk: AI-industry search terms and selected insight IDs are sent to the Jiqizhixin API.

Mitigation: Install only when that data sharing is acceptable, avoid sensitive queries, and treat JQZX_API_TOKEN as a secret.

Risk: Credential forwarding across redirects could expose the API token outside the intended service path.

Mitigation: Review the scripts before deployment and prefer a version that removes unsafe credential forwarding across redirects.

## Reference(s):

- [/api/v1 insight API strategy](artifact/references/api-v1-insights.md)
- [AI search keyword synonym reference](artifact/references/keyword_reference.md)
- [Jiqizhixin data service](https://www.jiqizhixin.com/data-service)
- [Jiqizhixin API base URL](https://mcp.applications.jiqizhixin.com)
- [ClawHub skill page](https://clawhub.ai/jiqizhixin/skills/ai-insight-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with source-linked evidence, optional shell commands, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require JQZX_API_TOKEN and curl to retrieve insight search results and detail records.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
