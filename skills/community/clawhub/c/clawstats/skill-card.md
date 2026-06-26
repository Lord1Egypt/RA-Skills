## Description: <br>
Monitor CPU, RAM, disk space, temperature, load average, and top processes on OpenClaw systems using a single versatile script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aprilox](https://clawhub.ai/user/Aprilox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect local OpenClaw host health from an agent session, including resource usage, load average, temperature, and top process names. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal local resource usage, disk usage, load averages, temperature, and top process names to an agent session. <br>
Mitigation: Install it only on systems where that operational visibility is acceptable. <br>
Risk: The skill requires making a local shell script executable. <br>
Mitigation: Review monitor.sh before enabling execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Aprilox/clawstats) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain-text terminal output from monitor.sh commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command modes include cpu, ram, disk, temp, top, and all.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
