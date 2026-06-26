## Description: <br>
Track lab equipment calibration dates and send maintenance reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanruoyu](https://clawhub.ai/user/shanruoyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lab staff and operations teams use this skill to add equipment records, list calibration schedules, and check for overdue or upcoming maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Equipment names, calibration dates, intervals, and optional locations are retained locally in ~/.openclaw/equipment_log.json. <br>
Mitigation: Review the stored records for local policy fit and delete ~/.openclaw/equipment_log.json when the retained maintenance data is no longer needed. <br>
Risk: Maintenance reminders are produced only when the user runs the check command. <br>
Mitigation: Run the check workflow on a planned schedule and treat the alerts as manual maintenance prompts, not automatic notifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shanruoyu/equipment-maintenance-log) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [CLI text output with local JSON record storage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores equipment names, calibration dates, intervals, and optional locations in ~/.openclaw/equipment_log.json; no external Python packages are required.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
