## Description: <br>
Crisis Detector helps agents identify self-harm, suicide ideation, and mental health crisis signals in user text, then surface severity, resources, alerts, and response guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and safety teams use this skill to add crisis-signal triage, resource routing, and escalation workflows to platforms that handle user-generated communication. It is especially sensitive because it may influence monitoring, outreach, emergency-contact notification, or authority escalation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive mental-health monitoring may occur without enough user control or clear notice. <br>
Mitigation: Deploy only with explicit user notice and consent, a clear way to stop or reduce monitoring, and documented data minimization practices. <br>
Risk: Automated crisis detection can produce false positives, false negatives, or inappropriate escalation. <br>
Mitigation: Require trained human review before emergency-contact or authority escalation, and maintain escalation procedures that account for uncertainty. <br>
Risk: Crisis alerts and user-status data can expose highly sensitive safety-team information. <br>
Mitigation: Use strict access controls, confidential logging, retention and deletion rules, and audit logs for all crisis-safety data. <br>
Risk: The release references an external npm package whose implementation is not verified by the provided evidence. <br>
Mitigation: Verify the external npm package, dependencies, and runtime behavior separately before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raghulpasupathi/crisis-detector) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, configuration, guidance] <br>
**Output Format:** [Markdown documentation with JSON configuration examples, JavaScript API examples, and crisis-response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include crisis severity labels, confidence scores, recommended actions, resource lists, alert instructions, and empathetic response text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
