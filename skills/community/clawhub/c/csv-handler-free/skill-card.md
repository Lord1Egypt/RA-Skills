## Description:

自动检测编码与分隔符，读取并清洗CSV数据，支持基础合并与导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and automation teams use this skill to inspect CSV files, detect encodings and delimiters, clean tabular data, and export results for reporting, analysis, or visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command execution for a workflow that is primarily local CSV processing.

Mitigation: Review proposed commands before execution and run only commands needed for local CSV inspection, cleaning, or export.

Risk: The security evidence notes API key and external API language without a clear CSV-related need.

Mitigation: Avoid providing API keys or other credentials unless a trusted workflow explicitly requires them.

Risk: The security verdict is suspicious because unrestricted command execution could expose local files or sensitive data.

Mitigation: Use the skill on trusted local CSV files in a sandboxed agent session with command approval enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/csv-handler-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose CSV profile summaries, cleaned data handling steps, export instructions, and error-handling guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
