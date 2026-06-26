## Description: <br>
Uses the official DeepL API for text translation, document translation, language and usage queries, and glossary v2/v3 management when the user explicitly requests DeepL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liaol99](https://clawhub.ai/user/liaol99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and users use this skill to call DeepL for explicit translation, rewriting, document translation, language support, quota, and glossary management tasks. It is appropriate when outputs should come from DeepL's official API rather than a general translation capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, documents, and glossary entries are sent to DeepL using the configured API key. <br>
Mitigation: Avoid submitting secrets or regulated data unless authorized, and use a dedicated DeepL API key where appropriate. <br>
Risk: Glossary update or delete commands can modify the wrong DeepL glossary if an incorrect ID is supplied. <br>
Mitigation: Confirm glossary IDs and language pairs before running update, replace, or delete commands. <br>
Risk: DeepL API behavior, limits, and response fields can vary by account type or change as the API evolves. <br>
Mitigation: Use --json for full responses when troubleshooting and compare behavior against the current DeepL API documentation. <br>


## Reference(s): <br>
- [DeepL API reference summary](references/deepl_api.md) <br>
- [DeepL API reference](https://developers.deepl.com/api-reference) <br>
- [DeepL Translate API](https://developers.deepl.com/api-reference/translate) <br>
- [DeepL Document API](https://developers.deepl.com/api-reference/document) <br>
- [DeepL usage and quota API](https://developers.deepl.com/api-reference/usage-and-quota/check-usage-and-limits) <br>
- [DeepL glossaries documentation](https://developers.deepl.com/docs/api-reference/glossaries) <br>
- [DeepL OpenAPI repository](https://github.com/DeepLcom/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance] <br>
**Output Format:** [Plain text or JSON responses, Markdown usage guidance, shell commands, configuration instructions, and translated document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DEEPL_API_KEY from the environment and can return full API structures when --json is requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
