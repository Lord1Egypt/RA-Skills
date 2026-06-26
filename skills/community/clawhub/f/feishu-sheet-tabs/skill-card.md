## Description: <br>
Create and organize multiple tabs inside an existing Feishu sheet when the normal feishu_sheet API cannot create new worksheet tabs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-Hanasq](https://clawhub.ai/user/G-Hanasq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to create, rename, inspect, and organize worksheet tabs in an existing Feishu spreadsheet, then return to feishu_sheet for structured data writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill acts through an authenticated Feishu browser session and can change spreadsheet structure. <br>
Mitigation: Confirm the exact spreadsheet URL, active workspace or account, current tabs, and intended tab changes before allowing browser automation to mutate the sheet. <br>
Risk: Browser runtime methods and visible controls can target the wrong tab or expose unexpected Feishu behavior. <br>
Mitigation: Inspect current sheet ids and names before mutation, prefer discovered runtime methods over blind UI clicking, and use returned tab ids for later writes. <br>
Risk: Artifact examples include a concrete spreadsheet token that should not be reused as a target. <br>
Mitigation: Use only the user's confirmed spreadsheet URL or token and do not treat example tokens as reusable credentials or destinations. <br>


## Reference(s): <br>
- [Runtime Notes](references/runtime-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/G-Hanasq/feishu-sheet-tabs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and a status summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports created or renamed tabs, discovered tab ids, whether data filling completed, and whether browser login or relay was required.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
