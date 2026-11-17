## Description:

Amazon Review Checker analyzes Amazon product reviews for authenticity signals including suspicious patterns, rating manipulation, content similarity, time clustering, and verified-purchase anomalies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and seller-support agents use this skill to review pasted or structured Amazon review data and summarize heuristic authenticity risks. It helps flag suspicious review clusters and explain which input fields would improve the analysis depth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report generator can execute unsafe injected HTML or JavaScript when used with untrusted review data.

Mitigation: Avoid generating or opening HTML reports from untrusted data until report fields are escaped and unsafe DOM insertion is removed.

Risk: The HTML report loads unpinned remote JavaScript.

Mitigation: Pin or vendor the JavaScript dependency before using generated reports in reviewed or production workflows.

Risk: Authenticity scores are heuristic and may overstate certainty.

Mitigation: Treat the score as triage guidance and review the flagged evidence before taking business action.

## Reference(s):

- [Amazon Review Checker on ClawHub](https://clawhub.ai/phheng/skills/amazon-review-checker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style analysis summaries with optional command examples and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticity scoring is heuristic and depends on the review fields supplied by the user.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
