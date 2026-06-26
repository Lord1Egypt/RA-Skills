## Description: <br>
Converts prepared Markdown or text into Chinese official-document DOCX files and can optionally produce PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Blicae8917](https://clawhub.ai/user/Blicae8917) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to turn already prepared Markdown or text into formal Chinese government-style documents such as reports, notices, plans, briefings, opinions, and meeting minutes. It handles document formatting and conversion, not content planning or approval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF conversion runs LibreOffice and may load locally compiled native code from a shared temporary location. <br>
Mitigation: Prefer DOCX-only output when PDF is not required, run without elevated privileges, and use a trusted isolated workspace. <br>
Risk: Document conversion depends on local binaries, so missing or untrusted dependencies can cause failures or unsafe execution. <br>
Mitigation: Install only if the publisher is trusted, verify python3, gcc, and soffice are expected on the host, and review generated DOCX or PDF files before distribution. <br>


## Reference(s): <br>
- [Official format rules](references/official-format-rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/Blicae8917/8917-docx-official) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DOCX or PDF files plus a Markdown response with output paths or conversion errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PDF output requires LibreOffice; the artifact declares python3, gcc, and soffice runtime dependencies.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
