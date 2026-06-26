## Description: <br>
Feishu Room Booking helps agents query room availability, reserve meeting rooms, manage room preferences, scan calendars for missing rooms, and maintain waitlists for ByteDance-internal Feishu users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiushibang](https://clawhub.ai/user/qiushibang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees use this skill to find and reserve Feishu meeting rooms, apply personal room preferences, and remediate accepted calendar events that lack a confirmed room. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically change calendar room reservations during scans or waitlist processing without fresh user confirmation. <br>
Mitigation: Use confirm-before-booking or dry-run mode for scans and waitlists unless the deployment explicitly allows automatic room remediation. <br>
Risk: The skill requires Feishu calendar and resource-booking authority and includes local preference data. <br>
Mitigation: Install only in trusted Feishu environments, remove bundled real user preference data before release, and restrict preference list or delete actions to trusted administrators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiushibang/feishu-room-booking) <br>
- [room-mapping.json](references/room-mapping.json) <br>
- [user-preferences.json](references/user-preferences.json) <br>
- [room-waitlist.json](references/room-waitlist.json) <br>
- [weekly-workspace.json](references/weekly-workspace.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands plus JSON or table script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes room availability, booking status, waitlist state, and preference or workspace updates.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
