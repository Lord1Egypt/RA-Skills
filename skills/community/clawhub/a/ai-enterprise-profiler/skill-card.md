## Description:

AI 企业画像 helps AI practitioners build structured company profiles, competitor scans, financing summaries, team analyses, and comparison conclusions using the /api/v1/enterprises query interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiqizhixin](https://clawhub.ai/user/jiqizhixin)

### License/Terms of Use:

MIT-0

## Use Case:

AI researchers, investors, BD teams, market analysts, and strategy teams use this skill to research individual AI companies or compare companies across sectors. It supports structured profiles covering basic company facts, teams, products, financing, operating status, competitive position, and risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The query script can send JQZX_API_TOKEN to a BASE_URL override or redirected endpoint.

Mitigation: Keep BASE_URL unset unless the endpoint is trusted, avoid shared environments where others can control variables, and validate redirect destinations before sending credentials.

Risk: Company research results may be incomplete when the API returns too few candidates or narrow filters miss aliases.

Mitigation: Expand company aliases or query terms, disclose coverage boundaries, and use consistent fields when comparing companies.

## Reference(s):

- [/api/v1 enterprise interface strategy](references/api-v1-enterprises.md)
- [Search keyword synonym reference](references/keyword_reference.md)
- [Jiqizhixin data service](https://www.jiqizhixin.com/data-service)
- [Jiqizhixin enterprise API endpoint](https://mcp.applications.jiqizhixin.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, structured tables, JSON API request examples, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JQZX_API_TOKEN plus curl and jq when using the bundled query script.]

## Skill Version(s):

0.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
