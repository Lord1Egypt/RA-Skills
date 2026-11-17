## Description:

Activity Duration Estimation helps agents plan project work breakdown structures, estimate activity duration with PERT and Monte Carlo methods, draft project documents, run economic analysis, perform earned value management, and generate self-contained HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and agents use this skill to decompose project scope, estimate durations and dependencies, produce project-management documents, calculate economic metrics, and assess earned value for active projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist project data and settings and read or import external databases when asked.

Mitigation: Use trusted project files and databases, review what will be imported, and avoid storing sensitive project data unless the skill data directory is acceptable for that data.

Risk: The settings server exposes local network behavior that the security guidance flags as under-scoped.

Mitigation: Run the settings server only in trusted local environments and avoid exposing it on untrusted networks.

Risk: Generated reports should be treated as untrusted HTML until escaping and CDN integrity issues are fixed.

Mitigation: Review generated HTML before sharing or publishing it, and open reports in a constrained browser context when working with untrusted inputs.

Risk: Untrusted template or project names may affect generated reports or files.

Mitigation: Use reviewed template names and project names, especially before generating or distributing reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/activity-duration-estimation)
- [Activity duration estimation methods](references/methods.md)
- [WBS methodology](references/wbs-methodology.md)
- [Project documents methodology](references/project-docs-methodology.md)
- [Economic analysis methodology](references/economic-analysis-methodology.md)
- [Earned value management methodology](references/evm-methodology.md)
- [Knowledge interface](references/knowledge-interface.md)
- [Search integration](references/search-integration.md)
- [Permissions and test summary](references/permissions.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python and shell snippets, structured project data, and generated HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist project data, settings, imported database content, and generated reports in the skill data directory.]

## Skill Version(s):

1.11.7 (source: server release evidence, SKILL.md frontmatter, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
