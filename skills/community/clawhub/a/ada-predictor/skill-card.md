## Description: <br>
Predicts anti-drug antibody risk for biologic therapy using clinical and genomic variables and returns a risk score, tier, and monitoring recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoReuMD](https://clawhub.ai/user/CryptoReuMD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, clinical researchers, and medically supervised agents use this skill to estimate patient-level ADA risk for TNF inhibitors and related biologics, then review monitoring and treatment-planning suggestions. Its output should support, not replace, qualified clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides treatment and monitoring suggestions for biologic therapy. <br>
Mitigation: Have a qualified clinician review all results before using them for diagnosis, methotrexate dosing, biologic switching, or monitoring schedules. <br>
Risk: Patient-level inputs may contain sensitive health information. <br>
Mitigation: Run the calculator only in a controlled local environment and avoid entering identifiable patient data unless that environment is authorized for it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CryptoReuMD/ada-predictor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and Python CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a 0-100 ADA risk score, risk tier, recommended TDM interval, clinical recommendation text, and Monte Carlo sensitivity statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
