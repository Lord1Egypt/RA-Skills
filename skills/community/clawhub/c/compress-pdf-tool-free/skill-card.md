## Description: <br>
This skill guides an agent to upload PDF files to a configurable compression API, tune image quality and DPI, poll job status, and return a download link for the compressed file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compress PDFs for archiving, email attachments, and upload-size limits by configuring quality, DPI, and an API endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads local PDFs and an API key to a configurable external endpoint. <br>
Mitigation: Review the API provider and endpoint before use, upload only PDFs that are appropriate for that service, and keep API keys out of logs and shared shell history. <br>
Risk: A configurable endpoint can create endpoint-safety and privacy exposure if pointed at an untrusted service. <br>
Mitigation: Prefer a fixed trusted HTTPS endpoint and review endpoint handling before using the skill with sensitive documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/compress-pdf-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples plus JSON/YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request configuration, job status text, and a compressed-file download link after polling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
