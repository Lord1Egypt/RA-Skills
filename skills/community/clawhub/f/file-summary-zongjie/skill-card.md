## Description: <br>
A bilingual OpenClaw skill that reads local txt, docx, pdf, xlsx, and xls files and returns extracted text for summary or analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonThePro2012](https://clawhub.ai/user/LeonThePro2012) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to extract text from local documents and ask the LLM to summarize or analyze the contents in Chinese or English. It is intended for local document review workflows where users can choose non-sensitive files and verify the generated summary or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local document contents may be sent into the OpenClaw LLM flow during summary or analysis. <br>
Mitigation: Use only files permitted by the user's data-handling policy, and avoid confidential, regulated, or highly private documents unless that policy allows this content flow. <br>
Risk: The Python helper can automatically install document-reading packages when dependencies are missing. <br>
Mitigation: Run the skill in a virtual environment or preinstall and review the required packages before use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/LeonThePro2012/file-summary-zongjie) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text content, summary text, analysis text, or bilingual error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports txt, docx, pdf, xlsx, and xls inputs; extracted document content may be sent into the OpenClaw LLM flow.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
