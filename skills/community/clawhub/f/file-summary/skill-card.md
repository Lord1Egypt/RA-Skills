## Description: <br>
Local document summary and analysis tool that extracts text from txt, docx, pdf, xlsx, and xls files for summarization in OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonThePro2012](https://clawhub.ai/user/LeonThePro2012) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to summarize local documents they explicitly select. It is intended for txt, docx, pdf, xlsx, and xls files where the agent should extract readable text and produce a concise summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local files selected for summarization. <br>
Mitigation: Install only if you are comfortable granting access to the local files you explicitly ask it to summarize. <br>
Risk: The skill may install Python dependencies in the active environment. <br>
Mitigation: Use it in a trusted Python environment, and review or preinstall the listed dependencies if supply-chain control matters. <br>
Risk: Extracted document content may be summarized through the configured OpenClaw LLM setup. <br>
Mitigation: Avoid confidential documents unless the OpenClaw and LLM provider configuration is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LeonThePro2012/file-summary) <br>
- [Publisher profile](https://clawhub.ai/user/LeonThePro2012) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text content, summaries, or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports txt, docx, pdf, xlsx, and xls inputs through local Python execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
