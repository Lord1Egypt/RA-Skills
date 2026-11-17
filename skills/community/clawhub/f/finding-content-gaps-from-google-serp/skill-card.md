## Description:

Finds content gaps and keyword opportunities by analyzing Google SERP results with apidojo's Google Search scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

SEO strategists, content marketers, and blog editors use this skill to prioritize content investments by finding weak, outdated, thin, or underserved Google search results for target keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The REST fallback places the Apify API token in a URL, where it may be captured in logs or shell history.

Mitigation: Prefer Apify MCP or a command that sends the token in an Authorization header, use a narrowly scoped Apify token, and avoid shell or debug logging around credentials.

Risk: Saved SERP exports may disclose keyword research or be written to unintended paths.

Mitigation: Choose output file paths deliberately and review exported CSV or JSON files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-content-gaps-from-google-serp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables and recommended content briefs; optional CSV or JSON result files from the Apify run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes keyword opportunity tiers, SERP quality scores, gap analysis, and recommended content angles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
