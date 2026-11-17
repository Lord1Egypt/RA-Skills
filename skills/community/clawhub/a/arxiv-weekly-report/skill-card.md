## Description:

Searches recent arXiv papers by subject category and keywords, identifies key contributions, and generates a structured Chinese Markdown weekly report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shu-ang](https://clawhub.ai/user/shu-ang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical teams use this skill to track recent arXiv papers by category and keyword, screen relevant papers, summarize methods and contributions, and save a reusable Chinese weekly research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PDF extraction utility can fetch arbitrary URLs and write cached files beyond the core arXiv reporting workflow.

Mitigation: Prefer arXiv IDs or arXiv-generated PDF links, avoid arbitrary --pdf-url values, and run extraction in a constrained workspace.

Risk: Persistent report and cache files may contain downloaded PDFs, extracted paper text, or research notes.

Mitigation: Use approved storage locations for generated reports and clean report/cache directories when retained files are no longer needed.

Risk: The PDF extraction dependency is not pinned in the artifact instructions.

Mitigation: Install pypdf in an isolated virtual environment and pin or review the dependency before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shu-ang/skills/arxiv-weekly-report)
- [arXiv API Query Endpoint](https://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown report with JSON script outputs and optional extracted text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved as Markdown files; optional PDF extraction can save cached PDF and text files.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
