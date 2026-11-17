## Description:

A Chinese-language business marketing content helper that generates search terms, industry Q&A terms, GEO-oriented Q&A knowledge-base prompts, and structured company information from Word documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuyingkj-coder](https://clawhub.ai/user/shuyingkj-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, content operators, and developers use this skill to prepare Chinese-language search optimization terms, FAQ-style knowledge-base content, and company profile material from business inputs and Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads user-selected Word documents and asks users to copy extracted content into Claude, which can expose confidential, regulated, or personal business data.

Mitigation: Use only appropriate source documents for the configured Claude environment and retention settings; avoid confidential, regulated, or personal data unless those controls are approved.

Risk: Document conversion depends on external Python tooling and may process untrusted DOCX content.

Mitigation: Pin and review dependencies, and run document conversion in a sandboxed environment for untrusted files.

Risk: Generated marketing and company-profile content may be inaccurate or misleading if source documents are incomplete or model output is not checked.

Mitigation: Manually review generated search terms, Q&A content, and company information before publishing or using it in customer-facing materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuyingkj-coder/skills/geo-optimization-cn)
- [Artifact README](artifact/README.md)
- [Quick reference](artifact/quickref.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Chinese-language plain text, Markdown prompts and content, command-line output, and optional DOCX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Word-document workflows read user-selected DOCX files, generate prompts for Claude, and can convert reviewed Markdown output into Word documents.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
