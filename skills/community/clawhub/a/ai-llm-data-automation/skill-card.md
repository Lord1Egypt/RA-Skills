## Description:

LLM数据自动化 helps users describe data-processing tasks in natural language so an agent can generate Python/Pandas code for Excel/CSV processing, PDF extraction, BIM data cleanup, and automated data pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and construction or operations teams use this skill to turn natural language data-processing requests into generated Python/Pandas workflows for cleaning, combining, extracting, and reporting on structured project data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes unsafe remote script execution for Ollama installation.

Mitigation: Use a verified installation method from a trusted source instead of copying the curl-to-shell command.

Risk: Generated Python/Pandas scripts can read, transform, and overwrite local files.

Mitigation: Run generated scripts on copied datasets or in a sandbox and inspect the code before using it on important files.

Risk: Cloud API use may expose confidential datasets, prompts, or business context.

Mitigation: Avoid sending sensitive data to the recommended cloud API unless its privacy and retention terms are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/ai-llm-data-automation)
- [ClawHub release homepage](https://clawhub.ai/yesong-Hue/ai-llm-data-automation)
- [Pandas documentation](https://pandas.pydata.org/docs/)
- [ShadowAI API referral](https://referer.shadowai.xyz/r/1056448)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated Python/Pandas code snippets and optional shell commands or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts may read and overwrite local data files; review and test them on copies before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
