## Description: <br>
Searches a corporate address book by organization path and job title after the user provides explicit query details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockcloud](https://clawhub.ai/user/blockcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized employees use this skill to look up address-book personnel records by organization path and job title, including employee identifiers and phone numbers when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose employee identifiers and phone numbers from an internal address book. <br>
Mitigation: Install and run it only when authorized for the address book, and do not share or retain returned employee details outside approved channels. <br>
Risk: Repeated, paginated, or multi-line searches can become bulk employee-data collection. <br>
Mitigation: Use narrow, business-justified queries and avoid broad or repeated lookups beyond the approved task. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown or plain text rows with organization, title, employee ID, name, desk phone, and mobile phone fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided organization and title details, user confirmation, and logged-in access before lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
