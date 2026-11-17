## Description:

Generate HTML code review pages with risk tags, diff highlights, and file-level annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn pull request diffs, file changes, and module walkthroughs into visual HTML review reports with risk tags, diff highlights, before/after comparisons, and file-level annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include untrusted PR, Git, file path, diff, or source text without explicit escaping requirements.

Mitigation: HTML-encode untrusted content, avoid raw HTML insertion and script/style/URL contexts, prefer no JavaScript or a restrictive CSP, and open reports in an isolated browser context.

## Reference(s):

- [Code Review Visualizer on ClawHub](https://clawhub.ai/paudyyin/skills/code-review-visualizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Self-contained HTML report with inline CSS and JavaScript, often described in Markdown or delivered as code for browser viewing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include PR summaries, risk maps, highlighted diffs, before/after comparisons, review guidance, module flow diagrams, and expandable code walkthroughs.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
