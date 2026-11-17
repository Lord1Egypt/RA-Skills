## Description:

Feishu Power Skill helps agents automate Feishu Bitable batch operations, cross-table queries, templated document generation, retail operations audits, and scheduled reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zj00777](https://clawhub.ai/user/zj00777)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to connect Feishu credentials, run Bitable workflows, generate Feishu documents from templates, audit retail data, and schedule recurring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scheduled report runner can execute a custom local Python script with the user's environment and Feishu credentials.

Mitigation: Install only after reviewing or removing the custom report runner, and run schedules only from trusted YAML files.

Risk: Feishu credentials and publication permissions can expose workspace data if over-scoped or shared accidentally.

Mitigation: Use a least-privilege Feishu app and keep FEISHU_APP_ID and FEISHU_APP_SECRET out of shared files and logs.

Risk: Scheduled or manual publishing can send generated reports to unintended Feishu destinations.

Mitigation: Review folder tokens and publish destinations before enabling scheduled publication.

Risk: Dependency installation may pull unpinned package versions into the active Python environment.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zj00777/skills/feishu-power-skill)
- [Feishu Open API Documentation](https://open.feishu.cn/open-apis)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON CLI output, YAML configuration, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local report files and publish documents to Feishu when explicitly configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
