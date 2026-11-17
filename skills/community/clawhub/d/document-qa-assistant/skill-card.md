## Description:

文档问答助手基于受信任的本地文档内容执行简单检索式问答，并返回答案、来源片段和置信度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to ask questions over trusted local documents and inspect returned source snippets. Use it for lightweight document lookup and summarization only after reviewing the documented security guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted PDF filenames can trigger arbitrary Python execution.

Mitigation: Only use the skill on documents and directories you fully trust, especially PDFs, and correct the PDF handling before normal installation or use.

Risk: The documentation overstates Word support, semantic retrieval, indexing, summaries, and cross-document validation.

Mitigation: Treat those claims as inaccurate until fixed and validate any answer, summary, or comparison against the source documents.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text answer with optional JSON result containing sources and confidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local document paths and a context-length parameter; returned claims and source snippets should be verified against the original documents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
