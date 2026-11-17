## Description:

Uses the official DeepL API for text translation, document translation, language and usage queries, text rephrasing, and glossary v2/v3 management when a user explicitly requests DeepL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liaol99](https://clawhub.ai/user/liaol99)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to call DeepL for explicit translation, rephrasing, document translation, language support, usage checks, and glossary management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected text, glossary entries, or documents are sent to DeepL under the user's DeepL account.

Mitigation: Use this skill only for content that is appropriate to send to DeepL, and confirm the account and data-handling requirements before translating sensitive material.

Risk: Glossary delete, replace, or update commands can modify remote DeepL glossary data.

Mitigation: Review glossary IDs, language pairs, and entries before running management commands, especially delete, PUT, and PATCH operations.

Risk: Document translation can write output files to local paths selected by the user.

Mitigation: Choose output paths deliberately and check for existing files before using document download or one-step document translation commands.

## Reference(s):

- [DeepL API Reference Summary](references/deepl_api.md)
- [DeepL API Reference](https://developers.deepl.com/api-reference)
- [DeepL Translate API](https://developers.deepl.com/api-reference/translate)
- [DeepL Document Translation API](https://developers.deepl.com/api-reference/document)
- [DeepL Usage and Quota API](https://developers.deepl.com/api-reference/usage-and-quota/check-usage-and-limits)
- [DeepL Glossaries API](https://developers.deepl.com/docs/api-reference/glossaries)
- [DeepL OpenAPI Repository](https://github.com/DeepLcom/openapi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON, Markdown with shell commands, and downloaded document files when document translation is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the DeepL API with user-selected text, glossary entries, or documents and may write translated document output files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
