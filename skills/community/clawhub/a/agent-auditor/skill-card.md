## Description: <br>
Audit any AI coding tool for telemetry, remote control, permissions, privacy, and hidden features. Generates a graded report (A-F). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mackding](https://clawhub.ai/user/mackding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit AI coding tool source directories for telemetry, remote control mechanisms, permissions, privacy impact, network behavior, hidden features, and graded remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs external npm-based audit code against the source directory selected by the user. <br>
Mitigation: Run it only on a narrow intended project directory, and review or pin the @claws-shield npm packages before using it on sensitive code. <br>
Risk: Scanning broad directories can expose unrelated private files or secrets to the audit process. <br>
Mitigation: Avoid scanning home directories, monorepos with unrelated private material, or folders containing secrets unless that scope is intentional and approved. <br>


## Reference(s): <br>
- [Agent Auditor on ClawHub](https://clawhub.ai/mackding/agent-auditor) <br>
- [Publisher profile: mackding](https://clawhub.ai/user/mackding) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured audit report with grades, source evidence, findings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Overall A-F grade, numeric score, per-category grades, evidence locations, and actionable recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
