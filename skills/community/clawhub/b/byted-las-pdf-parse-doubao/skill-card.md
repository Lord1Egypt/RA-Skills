## Description:

Parses and reads PDF documents into structured Markdown text using Volcengine LAS Doubao AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to convert PDFs, including scanned or complex-layout documents, into Markdown/text and structured page details through a Volcengine LAS submit-and-poll workflow.

### Deployment Geography for Use:

Volcengine LAS regions cn-beijing and cn-shanghai

## Known Risks and Mitigations:

Risk: Documents and parsed outputs may be sent to Volcengine/TOS cloud services.

Mitigation: Use the skill only with documents approved for that service, and avoid sensitive workspaces unless the data handling path has been reviewed.

Risk: The environment initialization script can auto-upgrade SDK code from a remote wheel during normal use.

Mitigation: Prefer a pinned and verified SDK package, or review the remote package source and hash before enabling automatic installation.

Risk: The workflow relies on local credentials such as LAS_API_KEY and optional Volcengine access keys.

Mitigation: Keep credentials in controlled environment variables or reviewed secret files, and avoid executable shell content in .env or env.sh files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-las-pdf-parse-doubao)
- [Publisher Profile](https://clawhub.ai/user/volcengine-skills)
- [API Reference](references/api.md)
- [Pricing Reference](references/prices.md)
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON results with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include parsed Markdown, per-page structured details, task status, local output paths, and optional presigned download links.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
