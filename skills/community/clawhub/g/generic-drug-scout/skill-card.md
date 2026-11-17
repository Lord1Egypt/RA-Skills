## Description:

Generic Drug Scout V1 creates static, interactive HTML reports or pre-seeded screening pages for China small-molecule crystal-form patent expiry opportunity scouting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to run a narrow first-pass screening workflow for China small-molecule crystal-form patent expiry opportunities and receive a local interactive HTML report. The workflow requires intended PatSnap MCP access for live database-backed screening, while sample data is reserved for UI preview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local Codex MCP configuration and is intended to call PatSnap MCP services.

Mitigation: Install and run it only in a workspace where PatSnap MCP access is intended and authorized.

Risk: Overwrite workflows can replace an existing target directory.

Mitigation: Use --overwrite only with a dedicated output folder, and do not point --target at existing project or home directories.

Risk: Generated HTML and CSV can contain data returned from external services.

Mitigation: Treat generated report files as untrusted content until serialization and export concerns have been reviewed and fixed.

## Reference(s):

- [V1 Scope](references/v1-scope.md)
- [Sample Report Data](references/sample-report-data.json)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap MCP Server Marketplace](https://open.zhihuiya.com/marketplace/mcp-servers)
- [PatSnap Developer Documentation](https://open.patsnap.com/devportal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples plus generated local HTML, JSON, CSV, and report assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are local files; live screening depends on configured PatSnap MCP services.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
