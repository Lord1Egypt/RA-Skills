## Description: <br>
CareMax OCR uploads medical report files to the CareMax Health API, runs OCR on the same session, streams progress, and helps agents review and save extracted structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittenyang](https://clawhub.ai/user/kittenyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to upload medical PDFs and images, run CareMax OCR, review extracted lab, genetic, imaging, pathology, or other report data, and confirm records only after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive medical reports and sends them through CareMax upload and OCR workflows. <br>
Mitigation: Use it only with reports the user is comfortable sending to CareMax, and confirm that the CareMax account and auth helper are appropriate before upload. <br>
Risk: The skill can delete individual health records or entire sessions. <br>
Mitigation: Require a separate explicit confirmation that names the exact session_id or record_id before running any delete operation. <br>
Risk: The skill depends on a sibling caremax-auth helper package for API calls and credential handling. <br>
Mitigation: Inspect and install the required caremax-auth helper before use, and stop if credentials are missing or unexpected. <br>


## Reference(s): <br>
- [CareMax OCR ClawHub listing](https://clawhub.ai/kittenyang/caremax-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams OCR progress line by line, summarizes extracted reports for review, and waits for approval before saving.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
