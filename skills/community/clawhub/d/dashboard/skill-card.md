## Description:

Build custom dashboards from any data source with local hosting and visual QA loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, operators, and business users use this skill to create local static dashboards, generated fetch scripts, and dashboard data/configuration files for user-selected data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated fetch scripts may mishandle API credentials or expose them locally if run without review.

Mitigation: Review generated fetch scripts before running them or adding them to cron, use restricted read-only API keys, and provide secrets through environment variables.

Risk: Dashboard data files may contain sensitive business or personal data on the local filesystem.

Mitigation: Keep dashboard directories and data files private, avoid displaying PII, and do not expose the local dashboard to a network without authentication.

## Reference(s):

- [Dashboard Skill Page](https://clawhub.ai/ivangdavila/skills/dashboard)
- [Data Sources by Use Case](artifact/sources.md)
- [Dashboard Design Rules](artifact/design.md)
- [Dashboard Widgets](artifact/widgets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with generated HTML, JSON configuration, data files, and shell script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local dashboard directories and user-run fetch workflows.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
