## Description:

Checks PDF, Word, and image project documents for completeness, timeliness, and visual compliance indicators such as seals and signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evob-z](https://clawhub.ai/user/evob-z)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to review project, invoice, or administrative approval documents for required files, validity dates, and visual indicators such as seals and signatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional exec SecretRef provider can run local commands and may expose the process environment.

Mitigation: Prefer env or file SecretRef providers; allow exec only for administrator-approved commands with an explicit minimal passEnv allowlist.

Risk: Sensitive documents or extracted content may be sent to configured vision, OCR, LLM, or embedding endpoints.

Mitigation: Use local OCR, private or local model endpoints, and redact sensitive content before remote processing.

Risk: Visual detection and compliance results are advisory and may be wrong or affected by unusual target text.

Mitigation: Treat results as decision support and require human review for compliance decisions, especially for unusual targets or high-impact documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evob-z/skills/compliance-checker-light)
- [Qwen-VL DashScope quick start](https://help.aliyun.com/zh/dashscope/developer-reference/vl-plus-quick-start)
- [README](README.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and structured Python dictionary results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Python APIs return dictionaries for completeness, timeliness, visual inspection, and health-check results.]

## Skill Version(s):

1.1.6 (source: SKILL.md frontmatter, pyproject.toml, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
