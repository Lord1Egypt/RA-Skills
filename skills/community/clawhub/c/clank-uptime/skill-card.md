## Description: <br>
Tracks website uptime, response times, and availability with CSV-based history, 24-hour stats, visual bars, and average/minimum/maximum latency as a lightweight alternative to paid monitoring services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t3mr0i](https://clawhub.ai/user/t3mr0i) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site owners use this skill to add monitored URLs, run uptime checks, inspect 24-hour availability and latency stats, and maintain simple local monitoring history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored URLs and timestamp, status, and response-time history are stored locally in ~/.clank-uptime. <br>
Mitigation: Add only URLs acceptable for local storage, and manage file permissions and retention for the ~/.clank-uptime directory. <br>
Risk: Automated checks can continue on a schedule if the user adds cron entries. <br>
Mitigation: Review the monitored site list and cron schedule before enabling automation, and remove cron entries when scheduled checks are no longer intended. <br>


## Reference(s): <br>
- [Clank Uptime on ClawHub](https://clawhub.ai/t3mr0i/clank-uptime) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and command output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and python3; stores monitored site configuration and CSV history under ~/.clank-uptime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
