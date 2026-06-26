## Description: <br>
Monitors CPU, memory, disk, network, uptime, process status, and threshold alerts for local system health reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local Linux host health, monitor resource usage continuously, configure simple threshold alerts, and export status snapshots as JSON for dashboards or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process listings and JSON status output can expose sensitive command-line arguments, secrets, usernames, or internal filesystem paths. <br>
Mitigation: Review and redact monitor output before sharing it outside the intended operational context. <br>
Risk: The skill inspects local host metrics and process details. <br>
Mitigation: Install and run it only in environments where local system inspection is acceptable. <br>
Risk: Continuous watch mode keeps collecting and displaying system status until stopped. <br>
Mitigation: Stop watch mode when monitoring is complete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash examples; monitor output is plain text status or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Watch mode streams repeated status snapshots until stopped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
