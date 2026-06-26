## Description: <br>
Helps OpenClaw users recommend meeting times, manage Feishu calendar events in batches, and generate meeting reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2389275723](https://clawhub.ai/user/2389275723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this skill to find available meeting slots, coordinate Feishu calendar changes, and produce meeting utilization reports for enterprise scheduling workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Developer-only publishing and license-management tooling may expose credentials or perform broad upload behavior. <br>
Mitigation: Review or remove scripts/api_publisher.py, scripts/license_manager.py, and other developer-only files before installation. <br>
Risk: Bulk calendar operations could create, modify, cancel, or notify attendees for the wrong meetings. <br>
Mitigation: Require explicit previews and user confirmation before any bulk calendar changes or attendee notifications. <br>
Risk: Calendar data and report exports may include sensitive scheduling information. <br>
Mitigation: Limit local caching and report exports to approved data, storage locations, and retention periods. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/2389275723/feishu-calendar-scheduler) <br>
- [Feishu Calendar Scheduler Documentation](https://docs.clawhub.com/skills/feishu-calendar-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce meeting-time recommendations, batch scheduling instructions, report-generation commands, and local configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
