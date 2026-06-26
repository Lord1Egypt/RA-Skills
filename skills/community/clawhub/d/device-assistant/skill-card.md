## Description: <br>
Device Assistant is a personal device and appliance manager for tracking device details, manuals, warranties, maintenance, and error-code troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
People managing home devices and appliances use this skill to record device inventory details, look up error codes, find manuals or support links, track warranty status, and maintain service logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Device inventory stored in workspace memory can include sensitive household or asset details such as model numbers, serial numbers, purchase data, locations, notes, warranty information, and maintenance history. <br>
Mitigation: Store only details needed for troubleshooting and warranty tracking, avoid full serial numbers when possible, and review workspace memory access before installing. <br>
Risk: Generated manual, search, or support links may disclose model numbers, error codes, or problem descriptions to external services if opened. <br>
Mitigation: Review generated links before opening them and remove unnecessary identifying details from searches. <br>


## Reference(s): <br>
- [Device Assistant ClawHub release](https://clawhub.ai/udiedrichsen/device-assistant) <br>
- [udiedrichsen ClawHub profile](https://clawhub.ai/user/udiedrichsen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write device inventory, error history, maintenance logs, cached error lookup data, and generated manual/search/support URLs under workspace memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
