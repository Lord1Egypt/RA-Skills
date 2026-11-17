## Description:

Advanced codebase analysis with HTML reports, git-aware diffs, trend tracking, SVG badges, CSV export, and CI/CD integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, open-source maintainers, and CI pipelines use this skill to inspect repositories, measure language and line-count metrics, generate reports, compare codebase snapshots, and track trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloading and running the script from a moving branch can execute code that differs from the reviewed release.

Mitigation: Use the bundled reviewed artifact or a pinned release, and inspect the script before running it.

Risk: Running repository analysis on untrusted projects can expose sensitive project metadata in generated reports or snapshots.

Mitigation: Run the tool in an isolated environment without secrets, and handle HTML reports and .codebase-snapshots as potentially sensitive outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/itspremkumar/skills/codebase-inspection)
- [Publisher Profile](https://clawhub.ai/user/itspremkumar)
- [Project Repository](https://github.com/itsPremkumar/codebase-inspection)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated text, JSON, CSV, HTML, SVG badge, and snapshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce repository metrics, language breakdowns, largest-file lists, diffs, trend snapshots, CI checks, and report files.]

## Skill Version(s):

2.0.1 (source: server-resolved ClawHub release metadata; artifact frontmatter and tool constant report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
