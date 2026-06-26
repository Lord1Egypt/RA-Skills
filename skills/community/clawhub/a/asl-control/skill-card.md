## Description: <br>
Monitor and control AllStar Link amateur radio nodes via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KJ5IRQ](https://clawhub.ai/user/KJ5IRQ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amateur radio operators and station maintainers use this skill to check ASL3 node status, inspect connected nodes, connect or disconnect remote nodes, manage favorites, and run timed net sessions through an existing ASL Agent REST API backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control live ASL node connections through API-key-authenticated connect and disconnect commands. <br>
Mitigation: Use it only with a trusted ASL Agent backend, protect ASL_API_KEY, and review generated commands before execution. <br>
Risk: The shell helper contains a fallback IP address that may be used if ASL_PI_IP is not set. <br>
Mitigation: Set ASL_PI_IP or ASL_API_BASE explicitly before use, or remove the fallback from asl-api.sh. <br>
Risk: Saved net sessions and cron-driven net tick commands can trigger later disconnect actions. <br>
Mitigation: Review state files and cron entries before enabling timed sessions, and clear stale sessions when no timed net should be active. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KJ5IRQ/asl-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; runtime commands emit JSON or short text output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus ASL_PI_IP or ASL_API_BASE and ASL_API_KEY environment configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
