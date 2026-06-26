## Description: <br>
Create price watch tasks and receive IM notifications when freight rates are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobofrivia](https://clawhub.ai/user/bobofrivia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freight and logistics users use this skill to create ocean freight price-watch tasks, confirm route and target-price details, and receive recurring notifications when matching rates are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Misconfigured Eyun server URL, company ID, or notification target could send freight-rate data to an unintended service or channel. <br>
Mitigation: Confirm the Eyun server URL, company ID, channel, and recipient are trusted and approved before installing or running the skill. <br>
Risk: The skill can register a recurring polling cron that continues sending rate notifications after setup. <br>
Mitigation: Review the eyun-watch-poll cron after setup and remove it if recurring polling or external chat delivery is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bobofrivia/eyun-watch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text guidance with shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May configure a recurring OpenClaw cron job for freight-rate polling and approved channel notifications.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
