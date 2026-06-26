## Description: <br>
Axioma Guard helps autonomous agents check ClawHub skills against Clawdex, report suspected threats, and generate advisory ethical vaccine responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan local skill directories, check a named skill before installation, and receive advisory status or mitigation text from configured security services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate its protection as an autonomous security control. <br>
Mitigation: Treat scan results and generated vaccine text as advisory, and review findings before installing or blocking skills. <br>
Risk: Skill names, scan targets, or threat details may be sent to external services. <br>
Mitigation: Confirm the configured CLAWDEX_API and MERLIN_API endpoints before use, and avoid sending internal skill names or sensitive threat details unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [Axioma Guard ClawHub page](https://clawhub.ai/kofna3369/axiomaguard) <br>
- [Clawdex skill API](https://clawdex.koi.security/api/skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text output with status messages and advisory mitigation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured CLAWDEX_API and MERLIN_API endpoints; results should be treated as advisory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
