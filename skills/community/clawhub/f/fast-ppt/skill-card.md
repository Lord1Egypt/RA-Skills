## Description: <br>
Fast PPT converts PDFs and documents into editable PPTX decks through the siping.me/pingPPT cloud service and returns a ppt.siping.me download link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use Fast PPT to turn PDF, Word, Markdown, or text documents into editable presentation decks. It supports AI theme layout and PDF-only conversion, with explicit user consent required before uploading files to the third-party cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User documents are uploaded to the siping.me/pingPPT cloud service for processing. <br>
Mitigation: Tell the user the file will leave their machine and get clear confirmation before every upload. <br>
Risk: Confidential, regulated, medical, financial, identity, customer, or contract-restricted documents may be inappropriate for third-party processing. <br>
Mitigation: Decline by default for sensitive files unless the user confirms they have permission and accepts the risk. <br>
Risk: AI theme mode may send document content to an LLM as part of slide generation. <br>
Mitigation: Explain the AI processing path and offer PDF-only conversion when the user wants to avoid LLM-based re-layout, while still noting that cloud upload is required. <br>
Risk: Generated download links are temporary and should not be treated as long-term storage. <br>
Mitigation: Tell the user to download the PPTX promptly and avoid using the link as a durable archive. <br>


## Reference(s): <br>
- [Fast PPT on ClawHub](https://clawhub.ai/sipingme/fast-ppt) <br>
- [pingPPT theme gallery](https://ppt.siping.me) <br>
- [Publisher profile](https://clawhub.ai/user/sipingme) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl command examples and download-link text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the API-provided ppt.siping.me download URL; optional local PPTX download is agent-controlled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
