## Description:

Analyzes and generates llms.txt files -- the emerging standard for helping AI systems understand website structure and content. Can validate existing llms.txt files or generate new ones from scratch by crawling the site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and content teams use this skill to validate an existing /llms.txt file or generate llms.txt and llms-full.txt content from a website crawl. It helps agents assess structure, page coverage, URL validity, and content quality for AI-facing site summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch and crawl the website domain provided by the user.

Mitigation: Use it only on public sites or sites the user is authorized to analyze.

Risk: Generated llms.txt files and analysis reports may contain incomplete or inaccurate site descriptions.

Mitigation: Review generated content, URL selections, and business facts before publishing.

Risk: The skill may write generated llms.txt or report files into the workspace.

Mitigation: Review file paths and generated outputs before committing or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/geo-llmstxt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown reports, llms.txt text, llms-full.txt text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch public website pages and write generated llms.txt or analysis report files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
