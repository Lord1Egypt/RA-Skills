## Description: <br>
Summarize Feishu/Lark cloud documents the user can read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victor-thu](https://clawhub.ai/user/victor-thu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to turn Feishu/Lark docx or wiki links they can access into structured in-chat summaries. It is intended for document understanding workflows where the user expects a concise summary without extra prompting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read Feishu/Lark documents that contain sensitive business or personal information. <br>
Mitigation: Use the skill only with documents the user is authorized to access, and treat generated summaries as sensitive when the source document is sensitive. <br>
Risk: Quoted evidence in a summary could be inaccurate if it is not grounded in the retrieved document text. <br>
Mitigation: Keep source quotes short and include only text that appears in the retrieved document. <br>
Risk: Permission failures or empty reads can lead to incomplete summaries. <br>
Mitigation: Ask the user to confirm read access before summarizing when document retrieval fails or returns empty content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/victor-thu/feishu-doc-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary in the current chat] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the original document link and short representative source quotes only when they appear in the document.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
