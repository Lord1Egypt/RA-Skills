## Description: <br>
Fetches WeChat public-account article links from the Dajiala API and saves them to an Excel file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mabao-laodie](https://clawhub.ai/user/mabao-laodie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and developers use this skill to collect article titles, links, publication times, and account names for configured WeChat public accounts through the Dajiala API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Dajiala API key and sends configured public-account IDs to Dajiala. <br>
Mitigation: Use only approved account lists and review Dajiala data-handling terms before processing confidential or sensitive lists. <br>
Risk: The skill writes Excel exports to a configured local directory. <br>
Mitigation: Set input and output paths appropriate for the deployment environment and restrict access to generated workbooks. <br>


## Reference(s): <br>
- [Dajiala API endpoint used by the skill](https://www.dajiala.com/fbmain/monitor/v3/post_condition) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [Excel workbook (.xlsx) with terminal status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workbook contains public-account name, article title, article link, and publication time fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
