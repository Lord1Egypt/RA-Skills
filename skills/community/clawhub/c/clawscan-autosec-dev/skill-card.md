## Description: <br>
ClawScan performs first-pass security checks for local OpenClaw deployments by checking version risk, installed skill hashes, and listener exposure through the ClawScan service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fate93930](https://clawhub.ai/user/fate93930) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use ClawScan to assess local OpenClaw deployments for known vulnerable versions, known malicious skill hashes, and potentially exposed listeners. It can run targeted checks, a combined scan, or scheduled monitoring that reports only when risk is found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan sends OpenClaw version data, installed skill names, relative paths, file hashes, and listener process/IP/port metadata to the ClawScan service. <br>
Mitigation: Install and run it only when that data sharing is acceptable for the target environment. <br>
Risk: Scheduled scans persist local schedule state and may continue checking without output when no risk is found. <br>
Mitigation: Enable scheduled scans deliberately, review the local schedule state, and disable the schedule when continuous monitoring is no longer wanted. <br>
Risk: A clean result means no known issue was matched, not that the OpenClaw environment is guaranteed safe. <br>
Mitigation: Treat ClawScan as a first-pass check and pair it with normal security review, dependency review, and external exposure validation where needed. <br>


## Reference(s): <br>
- [ClawScan API Contract](references/api-contract.md) <br>
- [ClawScan README](README.md) <br>
- [Project homepage](https://github.com/autosecdev/clawscan-skills) <br>
- [ClawHub skill page](https://clawhub.ai/fate93930/clawscan-autosec-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled scans may intentionally produce no output when every check is low risk and no actionable finding is present.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
