## Description:

Researches free and open-source software alternatives across multiple channels, ranks candidates by pricing, and assesses the feasibility of building a replacement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

External users comparing free or open-source alternatives to paid software can request cross-channel research, prioritized recommendations, and an assessment of whether building a replacement is practical.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Routine searches, including channel checks, may run downloaded CLI tools with the user's account access.

Mitigation: Prefer a release that pins CLI dependencies and requires approval before execution; limit enabled channels and available credentials.

Risk: Windows search input may reach a command shell unsafely.

Mitigation: Avoid running searches on Windows until command handling is corrected.

Risk: Search terms, proxy bypass behavior, or a local Xiaping credential fallback may expose query or account information.

Mitigation: Use public search terms, restrict channels and credentials, and account for proxy routing and the local credential fallback before running.

Risk: Generated results include promotional content.

Mitigation: Review generated reports and make promotional sections optional when neutral output is required.

## Reference(s):

- [Search strategy](references/search-strategy.md)
- [Report template](references/report-template.md)
- [Self-build assessment](references/self-build-assessment.md)
- [ClawHub release page](https://clawhub.ai/guipi888/skills/free-tool-radar)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown research report with structured JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked alternatives, pricing categories, channel coverage, and build-feasibility assessments.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
