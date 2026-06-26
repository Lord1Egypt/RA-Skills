## Description: <br>
Book Walker helps an agent read PDF documents interactively, navigate by page or block, search content, manage bookmarks, and optionally use OCR for scanned or hard-to-extract PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YoungAndSure](https://clawhub.ai/user/YoungAndSure) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to walk through long PDFs, resume reading progress, locate specific sections, search for keywords, and keep bookmarks while working in a local workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can list PDF filenames in the local workspace. <br>
Mitigation: Use it only in workspaces where exposing PDF filenames to the agent is acceptable. <br>
Risk: Extracted PDF text, reading state, and bookmarks may be cached locally. <br>
Mitigation: Avoid opening confidential PDFs unless local caching is acceptable, and clear the local cache when retained excerpts are no longer needed. <br>
Risk: Non-default templates can cause PDF blocks to be processed by the agent or model. <br>
Mitigation: Use the default direct-output template for sensitive PDFs, or review custom templates before applying them to confidential content. <br>


## Reference(s): <br>
- [Book Walker ClawHub Listing](https://clawhub.ai/YoungAndSure/book-walker) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text responses with optional structured payloads for agent-side template processing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include PDF excerpts, progress indicators, search results, bookmark lists, dependency installation commands, and template-processing payloads when a non-default template is selected.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
