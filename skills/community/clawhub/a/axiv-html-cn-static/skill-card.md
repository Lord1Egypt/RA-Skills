## Description:

This skill converts an arXiv paper HTML page into a local Chinese static HTML webpage while preserving figures, icons, CSS assets, paper metadata, and Chinese text produced from arxiv-paper-resolver-style section extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengyaofang](https://clawhub.ai/user/zhengyaofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to turn arXiv experimental HTML and Chinese Markdown into a local Chinese reading page. It helps preserve article metadata, figures, tables, formulas, CSS, PDF copies, and asset manifests for offline-oriented review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network downloads and generated HTML handling can expose users to avoidable network and active-content risks.

Mitigation: Review before installing, run in an isolated virtual environment or container, avoid sensitive networks, and inspect generated HTML before opening or sharing it.

Risk: Unpinned dependencies and broad downloads can make builds harder to reproduce or audit.

Mitigation: Prefer pinned dependencies, restrict downloads to trusted arXiv HTTPS hosts, and apply practical download size limits.

Risk: Embedded figure, table, and MathJax content may carry active-content or sanitization concerns.

Mitigation: Sanitize embedded figure and table HTML, and use local MathJax or an explicit CDN opt-in when preparing release workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhengyaofang/skills/axiv-html-cn-static)
- [Output contract](references/output_contract.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated local HTML, JSON, PDF, and asset files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an index.html page, localized assets, paper metadata JSON, asset manifest JSON, figure manifest JSON, and a downloaded PDF when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
