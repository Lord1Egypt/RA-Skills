## Description: <br>
Diagnoses OpenClaw configuration, dependency, service, permission, performance, and integration problems and can generate repair guidance or reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BetsyMalthus](https://clawhub.ai/user/BetsyMalthus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, OpenClaw users, and system administrators use this skill to troubleshoot OpenClaw setup and runtime issues, review suggested fixes, and produce console, JSON, or Markdown diagnostic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair mode can install packages, start or initialize OpenClaw services, and change file permissions. <br>
Mitigation: Run report-only diagnosis first, review each proposed fix, avoid `--auto-fix` and sudo unless the changes are expected, and back up OpenClaw configuration before repairs. <br>
Risk: Diagnostic reports may include local system, service, configuration, and issue details. <br>
Mitigation: Review generated reports before sharing them and remove sensitive host, path, or configuration values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BetsyMalthus/claw-problem-diagnoser) <br>
- [Project documentation](https://docs.claw-problem-diagnoser.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON, or Markdown reports with suggested shell commands and configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a report file when an output path is provided; repair mode can execute selected fixes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
