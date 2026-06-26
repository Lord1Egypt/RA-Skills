## Description: <br>
Search and manage private, local document collections (PDF, PPTX, DOCX) offline. Use when you need to find information within your private files, not for web research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[docsagent](https://clawhub.ai/user/docsagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users use this skill to index and search private local PDF, PPTX, and DOCX collections, then answer questions from retrieved document snippets with source citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search answers may expose snippets from private local documents to the current agent conversation. <br>
Mitigation: Index only intended local paths and include source paths in answers so users can verify what document content was used. <br>
Risk: Missing, stale, or incomplete local indexes can produce incomplete answers. <br>
Mitigation: Check index status and add or refresh the relevant document paths before relying on search results. <br>


## Reference(s): <br>
- [DocsAgent ClawHub Skill Page](https://clawhub.ai/docsagent/docsagent) <br>
- [DocsAgent GitHub Repository](https://github.com/docsagent/docsagent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and source-citation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should mention source file paths and page numbers when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
