## Description:

智能数据采集器 automates data collection, cleaning, transformation, and export from web pages, APIs, databases, and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxg852621787](https://clawhub.ai/user/dxg852621787)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this OpenClaw skill to collect data from web, API, database, and file sources, then clean, transform, schedule, and export the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file, network, and database access can collect or export data outside the intended scope.

Mitigation: Run in an isolated environment with explicit URL/domain allowlists, confined input/output directories, and read-only database accounts.

Risk: Credential and authentication support can expose sensitive tokens or database credentials if over-privileged.

Mitigation: Use least-privilege credentials, avoid hard-coded secrets, and rotate any credentials used during testing or deployment.

Risk: Recurring scheduled jobs can repeatedly access external services or local resources without ongoing review.

Mitigation: Keep scheduling disabled unless needed, review each configured job, and monitor outputs and logs.

Risk: Server provenance is unavailable and manual clone/install instructions may point to a source that does not match the validated release.

Mitigation: Install only the validated ClawHub release unless the publisher provides a pinned matching source for manual installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dxg852621787/skills/data-harvester)
- [Publisher Profile](https://clawhub.ai/user/dxg852621787)
- [OpenClaw Homepage](https://openclawx.asia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown or text responses with Python snippets and configuration; exported data files may be JSON, CSV, Excel, SQLite, or PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.12+, CLAWHUB_SITE, and scoped access to configured network, database, file, and scheduling resources.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.json; source files also contain 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
