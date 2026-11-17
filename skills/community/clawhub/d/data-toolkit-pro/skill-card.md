## Description:

数据工具箱专业版 helps data teams perform data analysis, reporting, statistical testing, data quality monitoring, workflow automation, advanced visualization, data lineage tracking, and multi-source connection optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, data analysts, and data engineers use this skill to guide agent-driven data workflows such as statistical analysis, data quality checks, report generation, workflow orchestration, visualization, and lineage review. It is not positioned for real-time stream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad read, write, and command execution authority can modify project files or run unintended data-processing scripts.

Mitigation: Use the skill only inside a limited project directory, review proposed scripts and commands before execution, and run only trusted inputs and configurations.

Risk: Workflow scheduling can create recurring jobs without enough user-control guardrails.

Mitigation: Review every scheduled job, DAG, checkpoint, retry policy, and notification target before enabling automation.

Risk: Data-source credentials and webhook tokens may be exposed if stored in scripts or configuration files.

Mitigation: Keep credentials in environment variables or a protected secret store and redact sensitive values from generated outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/data-toolkit-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce analysis summaries, workflow/configuration snippets, quality reports, visualization guidance, and command proposals for the host agent to review or execute.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
