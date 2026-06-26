## Description: <br>
Routes AI tasks to suitable models by balancing task complexity, cost, latency, quality, reliability, and feedback learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skynet-jawol](https://clawhub.ai/user/skynet-jawol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to select an AI model and provider for a task, inspect decision confidence and estimated cost, latency, and quality, and record feedback to improve future routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or proprietary task content may appear in local logs or temporary request files when OpenClaw invocation is used. <br>
Mitigation: Install only in environments where local logging and temporary-file permissions are controlled, and avoid sending secrets unless logging and cleanup behavior has been reviewed. <br>
Risk: The skill reads and writes local configuration and routing history, including broad admin and configuration controls. <br>
Mitigation: Review configuration paths, file permissions, retention settings, and backup behavior before enabling learning or persistent storage. <br>
Risk: Network health checks and provider integration behavior may not fit restricted environments. <br>
Mitigation: Confirm provider, network, and OpenClaw integration settings before deployment, and disable integrations that are not required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skynet-jawol/dynamic-model-router) <br>
- [Artifact README](artifact/README.md) <br>
- [ClawHub skill manifest](artifact/skill.json) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON-compatible routing decisions with selected model/provider, confidence, reasoning, estimated metrics, status, and configuration data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist routing history, performance metrics, feedback, configuration, logs, and prompt-bearing temporary request files when OpenClaw invocation is used.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, skill manifest, package.json, and changelog released 2026-03-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
