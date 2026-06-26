## Description: <br>
Answers questions based on the content of uploaded documents (PDF, DOCX, TXT), supporting individual files or entire folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anand2426](https://clawhub.ai/user/anand2426) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to extract text from supported document files or folders and ask an agent fact-focused questions about the contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected document contents are shown to the agent and may appear in terminal logs. <br>
Mitigation: Use single files or tightly scoped folders, avoid mixed confidential directories, and confirm the documents are appropriate for agent processing. <br>
Risk: The skill depends on a separate PDF reader skill and local Python libraries for some formats. <br>
Mitigation: Verify the PDF-reader skill and required Python dependencies before relying on PDF, DOCX, or XLSX extraction. <br>
Risk: Very long documents or questions that require distant context may produce incomplete answers. <br>
Mitigation: Ask focused questions and verify important answers against the source documents. <br>


## Reference(s): <br>
- [Usage Guide for Document Q&A Skill](references/usage_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text containing extracted document context and the user's question] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes a single file or folder; PDF support depends on the separate iyeque-pdf-reader-1.1.0 skill, and DOCX/XLSX extraction depends on Python libraries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
