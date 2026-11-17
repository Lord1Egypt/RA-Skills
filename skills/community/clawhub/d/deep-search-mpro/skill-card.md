## Description:

A professional deep-research and report-generation skill for company, product, industry, market, and AI-vendor analysis that uses agent web search/fetch workflows and consulting frameworks to produce Markdown and HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muqi98-michael](https://clawhub.ai/user/muqi98-michael)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external analysts, and developers use this skill to turn a research topic into a structured analysis framework, gather traceable web evidence, and generate consulting-style market, company, product, industry, or AI-tool reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill may guide agents toward web searches, report-file generation, and optional local scripts.

Mitigation: Review planned searches and generated files before use, and run optional scripts only in a controlled environment.

Risk: The security summary notes guidance that may load or run unverified local skills and scripts outside the package.

Mitigation: Verify referenced sibling skills and script paths before following them, especially hard-coded user-directory paths.

Risk: Optional Python scripts may require dependencies and network access for collection workflows.

Mitigation: Use a virtual environment with pinned dependencies, explicit network limits, and source-review before enabling live collection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muqi98-michael/skills/deep-search-mpro)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Deep research methodology](artifact/references/methodology/deep-research-methodology.md)
- [Analysis frameworks](artifact/references/methodology/analysis-frameworks.md)
- [Report writing guide](artifact/references/methodology/report-writing-guide.md)
- [Workflow phase 0 details](artifact/references/workflow/phase0-details.md)
- [Workflow phase 1 details](artifact/references/workflow/phase1-details.md)
- [Workflow phase 2 details](artifact/references/workflow/phase2-details.md)
- [Model reference index](artifact/references/models/README.md)
- [Search engine guide](artifact/references/technical/search-engines.md)
- [Data quality guidelines](artifact/references/technical/data-quality-guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and HTML reports, with optional shell commands and configuration guidance for supporting scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite sources, mark unavailable data explicitly, and avoid fabricated metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
