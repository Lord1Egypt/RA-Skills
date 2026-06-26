## Description: <br>
Baby Record helps users capture baby-care observations from Chinese conversation or photographed paper forms, store them as daily local JSON records, and query recent summaries and trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cake-26](https://clawhub.ai/user/cake-26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers and assistants use this skill to record temperature, jaundice, bathing, weight, sleep, feeding, diaper, symptom, and note data for a baby, then retrieve single-day records, date ranges, and trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baby-care and health details are stored in local JSON files. <br>
Mitigation: Use the skill only where local storage of this information is acceptable, and document retention and privacy expectations before routine use. <br>
Risk: The helper script can write or delete JSON files outside the intended data folder if custom directories or malformed date values are used. <br>
Mitigation: Avoid custom data directories and require YYYY-MM-DD date values until strict date and path validation and deletion safeguards are added. <br>
Risk: Photographed form extraction can misread health or care values. <br>
Mitigation: Confirm extracted values with the user before saving, as the skill instructions require. <br>


## Reference(s): <br>
- [Baby Record release page](https://clawhub.ai/cake-26/baby-record) <br>
- [Baby data schema reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Chinese conversational responses, Markdown tables or lists, shell commands, and JSON records or query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses one local JSON file per day and supports incremental updates for repeated entries on the same date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
