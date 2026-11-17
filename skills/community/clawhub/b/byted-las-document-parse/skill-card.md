## Description:

Byted Las Document Parse helps agents extract structured Markdown content, including text, tables, and images, from PDFs, standard images, scanned documents, and long screenshots using Volcengine LAS services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse local files, URLs, or TOS-hosted PDFs and images into Markdown with extracted images and structured result files. It is suited to document reading, OCR-like extraction, table recovery, and long-screenshot parsing workflows.

### Deployment Geography for Use:

Global, subject to Volcengine LAS service region configuration for cn-beijing or cn-shanghai endpoints.

## Known Risks and Mitigations:

Risk: Target documents, screenshots, extracted images, and parsed outputs may be sent to Volcengine LAS/TOS services.

Mitigation: Use the skill only for documents approved for external processing, and confirm user consent before submitting sensitive content.

Risk: LAS/TOS credentials and custom endpoints can grant broad access or redirect processing.

Mitigation: Use least-privilege credentials, avoid untrusted env.sh files, and verify endpoint settings before execution.

Risk: Remote result content is fetched and written locally during parsing workflows.

Mitigation: Review generated Markdown, downloaded images, and JSON outputs before using them in downstream workflows.

Risk: Long-image LLM cropping can involve additional image transmission.

Mitigation: Disable long-image LLM cropping when extra image transmission is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-las-document-parse)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)
- [API reference](references/api.md)
- [Command reference](references/commands.md)
- [Configuration guide](references/configuration.md)
- [Usage examples](references/usage-examples.md)
- [FAQ](references/faq.md)
- [Volcengine LAS API key documentation](https://www.volcengine.com/docs/6492/2191994?lang=zh)
- [Volcengine TOS credential documentation](https://www.volcengine.com/docs/6291/65568?lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON status objects, local result files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save parsed Markdown, extracted images, full JSON responses, and optional ZIP archives.]

## Skill Version(s):

1.0.0 (source: server release metadata and .well-known/skills/index.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
