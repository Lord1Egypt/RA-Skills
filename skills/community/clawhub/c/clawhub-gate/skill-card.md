## Description: <br>
ClawHub pre-publish security gate that runs local static analysis and ClawScan polling before releasing a skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to run shellcheck, bandit, ClawHub sync, and ClawScan status checks before publishing or updating ClawHub skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that the helper can publish or update a ClawHub skill even when the user asks for the documented local-only check. <br>
Mitigation: Run it only when publication is intended, fix the local-only flow to skip clawhub sync before local-only runs, and require explicit publish confirmation. <br>


## Reference(s): <br>
- [Clawhub Gate release page](https://clawhub.ai/freepengyang/clawhub-gate) <br>
- [clawhub_gate.sh](references/clawhub_gate.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires shellcheck, bandit, jq, python3, the clawhub CLI, and a logged-in ClawHub configuration for publish and scan polling.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
