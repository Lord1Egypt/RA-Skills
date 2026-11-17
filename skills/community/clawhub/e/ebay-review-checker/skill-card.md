## Description:

Analyzes eBay review and seller feedback data for authenticity signals such as timing clusters, repeated content, generic comments, and suspicious rating patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and e-commerce operators use this skill to inspect pasted or structured review data and receive heuristic authenticity scoring, detected red flags, and guidance on what additional review fields would improve analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is described as eBay-specific, while security evidence notes that much of the implementation is Amazon-oriented or generic review analysis.

Mitigation: Treat results as heuristic review-pattern signals, not authoritative eBay authenticity findings, and manually review conclusions before using them for seller or buyer decisions.

Risk: Generated HTML reports may be unsafe with untrusted review data and rely on an external Chart.js CDN dependency.

Mitigation: Avoid opening generated reports from untrusted data unless HTML escaping and dependency handling have been reviewed and fixed.

Risk: The installation guidance uses global installation.

Mitigation: Install from a pinned release or commit in an isolated environment and avoid global installation for evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/ebay-review-checker)
- [Publisher profile](https://clawhub.ai/user/phheng)
- [Nexscope AI](https://www.nexscope.ai/)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown-style analysis report text and optional HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required. Scores are heuristic and should not be treated as authoritative eBay seller or buyer decisions.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
