## Description:

Perform deep, concurrent web research using the Perplexity Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[holygrass](https://clawhub.ai/user/holygrass)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to have an agent decompose complex research requests into focused queries, retrieve current web results through Perplexity, and synthesize a cited Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned Python package at runtime.

Mitigation: Run it only in a sandbox where runtime package installation is acceptable, or preinstall and pin the Perplexity SDK before enabling the skill.

Risk: Research queries and retrieved context are sent to Perplexity using PERPLEXITY_API_KEY.

Mitigation: Avoid sensitive, confidential, or regulated research topics unless that data flow is acceptable, and scope the API key specifically to this use.

Risk: The runtime environment requires python3, network egress, and a writable package-install location.

Mitigation: Verify those runtime requirements in the target sandbox or bake dependencies into the image before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/holygrass/skills/echo-openclaw-perplexity-ultimate-async-deep-researcher)
- [Publisher profile](https://clawhub.ai/user/holygrass)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown research report with inline citations, plus Python code execution and JSON search-result parsing during the workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and PERPLEXITY_API_KEY; uses up to five concurrent Perplexity search queries and requests snippets capped at 2048 tokens per page.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
