## Description: <br>
Reviews outpatient chronic disease OCR record arrays for diabetes or hypertension and returns a review decision with supporting reasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaiccee](https://clawhub.ai/user/aaiccee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare operations teams and developers use this skill to run auxiliary chronic disease review checks on OCR-derived outpatient records and summarize the decision and reasoning. It is intended to support audit workflows, not to replace clinician judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical OCR contents may include sensitive patient information, and the security evidence says privacy promises are not enforced before data is sent to a remote service. <br>
Mitigation: Use the skill only when authorized to send the OCR contents to the configured backend, redact patient identifiers before use, verify the endpoint, and treat generated JSON and text outputs as sensitive medical records. <br>
Risk: The review decision and reasoning are auxiliary workflow outputs and may be incomplete or inappropriate for clinical decision-making. <br>
Mitigation: Require review by qualified clinical or audit staff before relying on the output for care, eligibility, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaiccee/chronic-disease-review) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Files] <br>
**Output Format:** [Raw JSON response file and natural-language text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes review output files locally and requires an OCR-array JSON input plus a diabetes or hypertension disease code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
