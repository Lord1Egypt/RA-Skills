## Description: <br>
智能电子书阅读助手，支持 EPUB/PDF 解析，并生成章节总结、关键摘录、深度分析和落地应用建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ludiansheng](https://clawhub.ai/user/ludiansheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, students, and knowledge workers use this skill to parse EPUB or PDF books and turn chapters into structured notes, excerpts, analysis, practical action plans, and follow-up reading suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill parses user-provided ebooks and PDFs, which may contain sensitive or restricted content. <br>
Mitigation: Use it only with files the user is comfortable having parsed and analyzed by the agent. <br>
Risk: Broad reading and note-taking triggers may activate the skill for unrelated note tasks. <br>
Mitigation: Confirm the request is for ebook or PDF reading before invoking the parser or applying the reading framework. <br>
Risk: PDF extraction can lose formatting, especially for scanned or complex-layout documents. <br>
Mitigation: Prefer EPUB or text-based PDFs, run OCR on scanned PDFs first, and review extracted text before relying on analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ludiansheng/ebook-reader) <br>
- [Reading analysis framework](references/reading-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reading notes and JSON parser output, with optional shell commands for parsing ebooks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports EPUB and text-based PDF parsing; scanned PDFs need OCR first for reliable analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, claw.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
