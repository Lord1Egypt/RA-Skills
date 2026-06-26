## Description: <br>
Queries Chinese holidays, work-shift arrangements, and workday status from local calendar files, with optional updates from configured public calendar sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claudecaicai](https://clawhub.ai/user/claudecaicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to check whether a China-specific date is a holiday, adjusted workday, or normal workday/rest day, and to update the local holiday calendar data when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Holiday data can become stale if the local calendar files are not updated. <br>
Mitigation: Run the provided update command when fresh holiday data is needed and verify the resulting calendar file before relying on it. <br>
Risk: Automatic monthly updates pull calendar data from configured public URLs. <br>
Mitigation: Review config.json, approve the iCloud and GitHub calendar sources for the environment, and keep any cron entry explicit and easy to disable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claudecaicai/cn-holiday-checker) <br>
- [Primary China holiday calendar source](https://calendars.icloud.com/holidays/cn_zh.ics) <br>
- [Backup China holidays calendar source](https://raw.githubusercontent.com/lanceliao/china-holidays/master/holidays.ics) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status messages and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Date checks accept YYYY-MM-DD input and return a workday/rest-day status with a short detail string.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
