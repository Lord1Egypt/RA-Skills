## Description:

Translate files (PDF, DOCX, PPTX) to any language using the Bluente Translation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[varsmallrookie](https://clawhub.ai/user/varsmallrookie)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to translate document files through the Bluente Translation API after providing an API key, source path, target language, and output location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload selected files or folders to a third-party translation service.

Mitigation: Run it only on documents the user is allowed to send to Bluente, and review folder contents before broad folder translation.

Risk: Translated output may overwrite or replace original documents when saved beside source files.

Mitigation: Prefer a separate output directory and keep backups of original files.

Risk: The Bluente API key may be written into generated scripts or logs.

Mitigation: Avoid storing generated scripts with embedded keys and rotate the key if it is exposed.

## Reference(s):

- [Bluente API documentation](https://www.bluente.com/docs)
- [Bluente API key settings](https://translate.bluente.com/settings/?type=apiKeys)
- [Bluente translation API base endpoint](https://api.bluente.com/api/20250924/blu_translate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python code and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create translated document files in a user-selected output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
