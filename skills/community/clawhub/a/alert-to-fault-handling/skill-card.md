## Description: <br>
Monitors alert context, matches alerts to configured remediation scripts, asks for confirmation, and reports execution results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lerwee](https://clawhub.ai/user/Lerwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers use this skill to triage infrastructure alerts in Feishu groups, recommend approved fault-handling scripts for matching alert categories, and run them only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run host remediation scripts and close alerts, while the security evidence notes weak built-in scoping. <br>
Mitigation: Review the external fault-handling and lerwee-api helpers before installation, limit the connected account to approved hosts, scripts, and alert actions, and require explicit operator confirmation before execution or alert closure. <br>
Risk: The artifact ships an execution log containing operational identifiers. <br>
Mitigation: Remove the bundled execution log before deployment and ensure runtime logs are access-controlled, protected, and rotated. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lerwee/alert-to-fault-handling) <br>
- [Lerwee publisher profile](https://clawhub.ai/user/Lerwee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style operational messages with inline shell command examples and JSON-backed configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute host remediation scripts and record JSON execution logs when invoked with confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
