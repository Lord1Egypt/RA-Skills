## Description:

Parses PDFs, Office files, images, and other documents with Baidu's document parsing API to extract text, tables, layout structure, OCR output, and RAG-ready chunks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maglanyulan](https://clawhub.ai/user/maglanyulan)

### License/Terms of Use:

MIT

## Use Case:

Developers and document-processing teams use this skill to submit supported documents to Baidu's intelligent document analysis API, poll asynchronous parsing jobs, and retrieve structured JSON or Markdown results for extraction, OCR, layout analysis, table parsing, and RAG chunking workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents or document URLs submitted through the skill are sent to Baidu for processing.

Mitigation: Use the skill only for documents approved for third-party processing, and avoid confidential, regulated, or credential-containing files unless the deployment has explicit approval.

Risk: Returned markdown_url and parse_result_url links remain sensitive while they are valid.

Mitigation: Restrict access to result links, avoid posting them in shared channels, and delete or rotate stored outputs according to local retention rules.

Risk: Baidu API keys can be exposed if committed to project settings or shared configuration files.

Mitigation: Store BAIDU_DOC_AI_API_KEY and BAIDU_DOC_AI_SECRET_KEY in a secure secret store or local environment and keep them out of source control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maglanyulan/skills/baidu-doc-pipeline-parser)
- [Baidu document parsing API documentation](https://ai.baidu.com/ai-doc/OCR/llxst5nn0)
- [Baidu intelligent document analysis platform](https://ai.baidu.com/solution/intelligent-document-analysis)
- [API key setup guide](references/apikey-fetch.md)
- [API parameters and response structure](references/parameters.md)
- [Error code reference](references/error_codes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return parsed document JSON, Markdown result links, and downloaded parse results from Baidu's asynchronous API.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
