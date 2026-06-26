## Description: <br>
Automatically evaluates task legality, ethical impact, risk level, and provides compliance suggestions with decision logging for AI assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BetsyMalthus](https://clawhub.ai/user/BetsyMalthus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, AI assistant operators, and compliance reviewers use this skill to evaluate requested tasks for legal, privacy, security, and ethical risk before execution. It returns risk level, compliance status, review requirements, warnings, issues, and recommended next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision logs can contain sensitive task descriptions and task details when logging or export is enabled. <br>
Mitigation: Disable decision logging for sensitive workflows when possible, clear logs regularly, and export logs only to trusted locations with appropriate file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BetsyMalthus/claw-ethics-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured Python objects or JSON containing risk level, compliance status, human review requirement, warnings, legal issues, ethical concerns, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can keep an in-memory decision log and export that log to a JSON file when enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
