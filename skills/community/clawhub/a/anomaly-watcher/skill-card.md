## Description: <br>
Continuous behavioral monitoring for OpenClaw agents. Detect anomalies in command patterns, resource usage, and skill invocations against established baselines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arhadnane](https://clawhub.ai/user/arhadnane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security operators use this skill to record agent activity, compare current behavior against rolling baselines, and surface anomalous command, file, network, skill, memory, and error patterns for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local monitoring logs may contain prompts, file paths, session IDs, or security findings. <br>
Mitigation: Use only in workspaces where local monitoring logs are acceptable; protect or exclude the .security directory from sharing and source control. <br>
Risk: Stored baseline and anomaly data may accumulate sensitive operational details over time. <br>
Mitigation: Periodically purge old logs according to the workspace retention policy. <br>
Risk: Anomaly classifications can be incomplete or noisy before enough baseline data exists. <br>
Mitigation: Treat alerts as review signals and allow the documented 48-hour calibration period before relying on baseline comparisons. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arhadnane/anomaly-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/arhadnane) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, Guidance] <br>
**Output Format:** [JSON responses with local JSONL monitoring logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records metrics and anomaly findings under the workspace .security directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
