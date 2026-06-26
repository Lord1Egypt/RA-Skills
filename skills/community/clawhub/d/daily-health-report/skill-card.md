## Description: <br>
Generates and publishes a daily Raspberry Pi system health report with uptime, memory, swap, load, disk, and temperature metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welderjustin](https://clawhub.ai/user/welderjustin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and developers use this skill to capture a scheduled health snapshot of a Raspberry Pi for quick review, channel posting, or operational logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release depends on a local health_report.sh script that is not included in the artifact. <br>
Mitigation: Inspect the local health_report.sh file before installing or scheduling the skill. <br>
Risk: Published reports may expose uptime, disk, memory, load, swap, and temperature details. <br>
Mitigation: Only enable scheduled runs or channel posting for destinations approved to receive host health details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/welderjustin/daily-health-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text report printed to stdout and saved as latest-health-report.txt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is generated from local system metrics at run time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
