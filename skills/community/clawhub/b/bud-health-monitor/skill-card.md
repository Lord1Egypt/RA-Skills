## Description: <br>
Monitor system health (RAM, disk, CPU, services), detect issues, and attempt fixes for Raspberry Pi and home server environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stigg86](https://clawhub.ai/user/stigg86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and home server operators use this skill to check RAM, disk, CPU, load, uptime, and high-memory processes on constrained Linux systems. It can also provide JSON status output and run remediation when intentionally invoked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fix mode can terminate unrelated high-memory processes. <br>
Mitigation: Use status, watch, or json for routine monitoring; review and narrow process-kill rules before enabling fix mode or cron automation. <br>
Risk: Fix mode may attempt privileged kernel cache changes. <br>
Mitigation: Install only when active remediation is intended and run privileged remediation manually until operational impact is understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stigg86/bud-health-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/stigg86) <br>
- [Project Homepage](https://github.com/stigg86/health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal text reports, JSON status output, and markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The status, watch, fix, and json commands report system health; fix mode may terminate processes and attempt cache cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
