## Description:

Checks running Docker containers for newer image versions, fetches release notes, and generates a prioritized update report that flags breaking changes versus safer updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect running Docker containers, compare Docker Hub image tags, fetch related release notes, and produce a prioritized update report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects running Docker containers and includes container metadata in generated reports.

Mitigation: Use it only in environments where that container metadata is acceptable to inspect and store.

Risk: The skill contacts Docker Hub and GitHub to check tags and fetch release notes.

Mitigation: Run it only when external registry and release-note lookups are acceptable for the environment.

Risk: Generated Markdown can include changelog text from external repositories.

Mitigation: Review reports before acting on update recommendations or sharing the output.

Risk: An optional GITHUB_TOKEN may increase API limits but introduces credential handling.

Mitigation: Set GITHUB_TOKEN only when needed and use a token with no unnecessary scopes.

Risk: Cron scheduling can repeatedly save reports to disk.

Mitigation: Enable scheduling only when recurring saved reports are intended and the destination path is appropriate.

## Reference(s):

- [Container Update Advisor Setup Guide](references/setup-guide.md)
- [Docker Hub API](https://hub.docker.com/v2)
- [GitHub REST API](https://api.github.com)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/container-update-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON intermediate data and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports prioritize updates by review-first versus safer patch-level changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
