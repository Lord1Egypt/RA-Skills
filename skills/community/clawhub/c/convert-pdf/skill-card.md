## Description: <br>
Convert web pages to PDF files using Playwright, saving them in A4 format with margins after fully loading the page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert a URL or short domain into a local PDF for offline reading, archiving, or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching a user-provided URL can expose network metadata and page access to the target site. <br>
Mitigation: Use trusted public URLs when possible and avoid sensitive internal pages unless that exposure is intended. <br>
Risk: A chosen output filename may overwrite an existing PDF path. <br>
Mitigation: Choose output filenames deliberately and check for existing files before conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/convert-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF file plus plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves an A4 PDF with 20px margins to the current working directory; a chosen existing PDF path may be overwritten.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
