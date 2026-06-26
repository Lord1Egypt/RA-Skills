## Description: <br>
Generates bidding data analysis reports from Excel files, including AI project share, annual trends, institution rankings, charts, and Word report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austin0208](https://clawhub.ai/user/austin0208) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement analysts, developers, and operational teams use this skill to process bidding spreadsheets and generate reports on AI-related procurement activity, yearly trends, and leading institutions. It is suited for university bidding, government procurement, and enterprise procurement analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Procurement spreadsheets may contain sensitive or confidential data. <br>
Mitigation: Run the skill locally in a controlled environment and review input files before processing or sharing generated reports. <br>
Risk: Unpinned Python dependencies may change behavior over time. <br>
Mitigation: Install in a virtual environment and lock dependency versions before production or sensitive-data use. <br>
Risk: PDF output is described in the artifact, but the security guidance says not to rely on it unless the publisher adds support. <br>
Mitigation: Use Word report output as the supported path and validate any PDF workflow separately before release use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/austin0208/bidding-analysis-report) <br>
- [Project homepage](https://github.com/openclaw/bidding-analysis-report) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with Python and shell examples; generated artifacts include Word documents and PNG charts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-provided Excel workbook and creates local chart images plus a Word report; PDF output is mentioned by the artifact but not supported by the security review guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
