## Description: <br>
China Summarizer helps agents summarize user-provided text, local TXT, Markdown, PDF, and Word files, web pages, news articles, and WeChat articles into concise Chinese summaries without requiring login or an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to extract and summarize user-provided Chinese or English articles, documents, web pages, and pasted text into structured Chinese summaries. It is especially useful when the user needs core points, key facts, and a one-sentence takeaway from long-form content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text, URLs, and local files may contain sensitive information that will be processed by the active model. <br>
Mitigation: Only provide content you are comfortable having the model process for summarization. <br>
Risk: The release declares capability tags for credentials, payment authority, and crypto access even though the visible summarization behavior does not need them. <br>
Mitigation: Do not grant credentials, payment authority, or crypto access when using this skill. <br>
Risk: Extraction may fail or be incomplete for JavaScript-rendered pages, scanned PDFs, unsupported Word formats, or missing local document parsers. <br>
Mitigation: Paste source text manually or install the documented parser tools only when needed, then review the generated summary against the source. <br>


## Reference(s): <br>
- [Content extraction technical notes](references/extract.md) <br>
- [Summarization prompt templates](references/prompts.md) <br>
- [ClawHub release page](https://clawhub.ai/tobewin/china-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary in Chinese with structured sections and bullets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves key figures, dates, names, and conclusions; long inputs are summarized in chunks before final synthesis.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
