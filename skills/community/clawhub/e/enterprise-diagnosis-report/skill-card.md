## Description: <br>
Generates a consolidated enterprise diagnosis report by parsing and integrating company profile, financial and tax diagnosis, and policy matching PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangl271](https://clawhub.ai/user/wangl271) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external advisers, and developers use this skill to combine enterprise diagnosis PDFs into a Markdown report covering company profile, financial and tax health, policy opportunities, data conflicts, and missing inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enterprise PDFs and generated outputs may contain financial, tax, or business-sensitive information. <br>
Mitigation: Use a dedicated working directory, restrict access to inputs and outputs, and delete or protect generated text and reports after use. <br>
Risk: The PDF parser can download PDFs from URLs, which may expose the agent to untrusted remote files. <br>
Mitigation: Prefer trusted local PDFs or known-good URLs, and avoid parsing unexpected or untrusted PDF links. <br>
Risk: Extracted tables, numbers, and policy matches can be incomplete or stale, especially for scanned PDFs or time-sensitive policy information. <br>
Mitigation: Review key figures, conflicts, missing fields, and current policy requirements before relying on the generated report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangl271/enterprise-diagnosis-report) <br>
- [Enterprise diagnosis report template](references/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with extracted text outputs and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted PDF text and generated reports to local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
