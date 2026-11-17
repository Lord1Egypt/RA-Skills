## Description:

China Summarizer summarizes Chinese or English content from pasted text, local TXT/MD/PDF/Word files, web pages, news articles, and WeChat articles into Chinese structured summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract and summarize user-provided documents, pasted text, and web articles into concise Chinese summaries that preserve key facts, names, dates, and numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read the local files or URLs that the user asks it to summarize, which can expose sensitive content to the active agent session.

Mitigation: Use the skill only with files and links the user intends to process, and review summaries carefully when source material is sensitive or untrusted.

Risk: Optional PDF and Word extraction tools or Python packages may need to be installed for some document types.

Mitigation: Install optional dependencies in a controlled environment without unnecessary administrator privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-summarizer)
- [Content extraction technical notes](references/extract.md)
- [Summary prompt templates](references/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-like Chinese structured summary with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long inputs may be summarized in chunks before final aggregation; summaries target 300-500 Chinese characters, with long-form summaries capped around 500 characters.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
