## Description: <br>
Guides agents through creating or translating Chinese OpenClaw skills, running quality checks, publishing them to ClawHub, and verifying the release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to prepare Chinese OpenClaw skills, run quality checks, publish them to ClawHub, and verify published versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact embeds an apparent live ClawHub token and shows account-changing publish commands. <br>
Mitigation: Remove the embedded token before use, rotate it if it could be real, and provide credentials through a safer login or environment-variable flow. <br>
Risk: The workflow supports batch publishing, which can propagate unreviewed skill content quickly. <br>
Mitigation: Review and scan every skill before batch publishing, and verify each published slug with ClawHub inspection. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes publishing workflow steps, evaluation criteria, command templates, checklists, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
