## Description:

Fetches webpage or API content, adaptively extracts key text, and prepares structured LLM summaries and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maplee](https://clawhub.ai/user/maplee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to fetch a user-specified public webpage or API endpoint, extract readable content and metadata, and prepare a structured report for LLM-assisted summarization and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, which may expose internal sites, private APIs, authenticated admin pages, cloud metadata endpoints, or secret-bearing pages if used without scoping.

Mitigation: Use it only with approved public URLs unless network access, authentication handling, and LLM safeguards are explicitly constrained for the deployment.

Risk: The declared local write and command-execution permissions increase the impact of misuse or compromised inputs.

Mitigation: Review and scan the skill before deployment, remove permissions that are not required, and run it in a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maplee/skills/adaptive-web-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown or JSON report with source details, extraction statistics, content preview, metadata, and structured LLM analysis guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one requested URL or API endpoint per run; extracted content is truncated to the configured maximum length.]

## Skill Version(s):

1.0.0 (source: artifact SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
