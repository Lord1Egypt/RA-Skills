## Description: <br>
Diagnoses whether a Cognitive Bullwhip Effect is already active in an agent system by tracing where small errors amplify into larger failures, scoring severity, and identifying the needed intervention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkc3080](https://clawhub.ai/user/jkc3080) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze recent agent decision history for variance amplification, locate the layer where errors begin to compound, score severity, and select a recommended intervention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decision logs can contain secrets, customer data, credentials, or unnecessary internal details. <br>
Mitigation: Redact sensitive data before use and provide only summarized decision history needed for diagnosis. <br>
Risk: The skill recommends linked paid remediation skills as part of its diagnostic output. <br>
Mitigation: Treat those recommendations as vendor suggestions and evaluate remediation choices independently before purchase or deployment. <br>
Risk: Diagnostic quality depends on a complete enough decision history for the variance scan. <br>
Mitigation: Run the skill on a representative observation window and verify important findings against agent logs before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkc3080/cognitive-bullwhip) <br>
- [AGDP skill homepage](https://agdp.io/agent/3387) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, text, guidance] <br>
**Output Format:** [JSON object with a plain-text diagnostic_report field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bullwhip status, severity score, amplification map, pattern type, recommended intervention, trace steps, and a human-readable diagnostic report.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
