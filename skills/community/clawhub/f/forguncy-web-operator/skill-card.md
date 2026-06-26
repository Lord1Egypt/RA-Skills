## Description: <br>
Provides functionality to interact with SpreadJS tables in the web applications built by Forguncy (aka 活字格), specifically for extracting table data and column headers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to read table names, CSV table contents, and column headers from authorized Forguncy web application pages opened in the browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return complete table contents from Forguncy pages the agent can access. <br>
Mitigation: Use it only on authorized pages and avoid extracting full tables that contain sensitive data unless that data is intended to be shared with the agent. <br>
Risk: Selecting the wrong Forguncy table name may extract unrelated page data. <br>
Mitigation: Deliberately inspect and choose the intended fgcname before running the table data or header extraction snippets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/forguncy-web-operator) <br>
- [Publisher profile](https://clawhub.ai/user/kadbbz) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown with JavaScript snippets and browser execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return complete table contents from pages the agent can access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
