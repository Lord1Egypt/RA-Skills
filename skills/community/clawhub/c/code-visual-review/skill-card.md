## Description:

Generate visual HTML pages for code review (diff + risk tags), code walkthrough (call chains + trust boundaries), and architecture analysis (module dependencies + tech debt). Three modes with shared dark-theme template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn diffs, file lists, or code entry points into visual review, walkthrough, and architecture reports. It helps reviewers explain risk, data flow, trust boundaries, dependencies, health scores, and technical debt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can expose sensitive source snippets, diffs, or credentials if shared beyond the intended review audience.

Mitigation: Remove secrets and sensitive code from inputs, then review generated reports before distributing them.

Risk: Untrusted diff or code content can create browser-facing risk if it is inserted into HTML without escaping.

Mitigation: Escape untrusted report content before opening generated HTML in a browser.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Self-contained HTML reports and Markdown PR descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include source snippets, diffs, risk labels, call chains, trust boundaries, Mermaid architecture diagrams, and technical debt summaries.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
