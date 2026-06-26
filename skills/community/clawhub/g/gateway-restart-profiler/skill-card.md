## Description: <br>
Profiles OpenClaw Gateway restart performance, diagnoses slow startup phases, and generates reports with optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tstj007](https://clawhub.ai/user/tstj007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to restart OpenClaw Gateway, monitor startup logs, identify slow phases, and produce performance reports for troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stop and restart OpenClaw Gateway, which may interrupt active work. <br>
Mitigation: Run it during a maintenance window and explicitly approve the restart before execution. <br>
Risk: The documented agent invocation uses elevated execution for the profiler. <br>
Mitigation: Avoid elevated mode unless it is necessary for the local OpenClaw installation. <br>
Risk: Generated reports may contain operational timing and log-derived details. <br>
Mitigation: Review generated text and HTML reports before sharing them outside the operating team. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, files, guidance] <br>
**Output Format:** [Console text plus generated text and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Restarts OpenClaw Gateway, monitors logs for up to about three minutes, and writes reports under the OpenClaw logs directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
