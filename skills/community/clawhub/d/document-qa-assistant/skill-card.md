## Description: <br>
文档问答助手。基于本地文档（PDF/Word/Markdown/TXT）回答问题，支持知识库检索和多文档交叉验证。当用户需要：从文档中查找答案、基于文档回答问题、跨多个文档综合查询、验证信息一致性、生成文档摘要时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to query local document files, retrieve relevant passages, summarize content, and compare information across documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF handling can turn an untrusted PDF filename into unintended Python code execution. <br>
Mitigation: Review or patch the PDF parser before use; avoid untrusted directories or PDFs with unusual filenames and prefer TXT or Markdown inputs until fixed. <br>
Risk: Several advertised capabilities are not included in the packaged artifact. <br>
Mitigation: Confirm required workflows against the packaged files before relying on features such as document indexing or unsupported file parsers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text answers with source snippets; optional JSON result from the packaged script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source file paths, line numbers, excerpts, scores, and a confidence value when JSON output is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
