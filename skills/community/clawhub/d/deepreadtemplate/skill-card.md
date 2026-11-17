## Description:

This skill helps an agent produce structured deep-read reports for academic papers from a PDF, DOI, arXiv link, title, or similar input, including full-text extraction when possible, exact-number quoting, method and result analysis, and visual report artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttggjj](https://clawhub.ai/user/ttggjj)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, graduate students, reviewers, and literature-review authors use this skill to turn academic papers into reusable deep-read reports that cover background, variables, methods, task flow, design details, statistical analysis, results, limitations, and implications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may download or search public copies of papers, which is inappropriate for sensitive unpublished manuscripts.

Mitigation: For sensitive manuscripts, provide the file directly and avoid asking the agent to search third-party mirrors.

Risk: If the full text is unavailable, the resulting report may be based only on abstracts or other public information.

Mitigation: Require the report to state when full text was not obtained and to mark inferred claims explicitly.

Risk: The default report can be broad and detailed when a shorter summary is needed.

Mitigation: Specify the preferred output language, depth, and summary length before invoking the workflow.

## Reference(s):

- [Deep Read Template](artifact/references/deep-read-template.md)
- [ClawHub skill page](https://clawhub.ai/ttggjj/skills/deepreadtemplate)
- [Publisher profile](https://clawhub.ai/user/ttggjj)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Guidance]

**Output Format:** [Markdown report plus self-contained HTML report with inline SVG diagrams and tables or charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks the agent to quote exact values from the source paper, mark inferences, and state when full text was unavailable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
