## Description: <br>
Calculates BMI, DuBois body surface area, WHO-style BMI categories, and optional BSA-based dose amounts from weight and height inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External clinicians, health operations users, and developers can use this local calculation aid to compute BMI, DuBois BSA, and simple BSA-based dose amounts. Medical or chemotherapy decisions should be independently verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation overstates pediatric, multi-formula, and drug-specific clinical workflows beyond the implemented calculator. <br>
Mitigation: Treat the release as a simple BMI and DuBois BSA calculator, and do not rely on advertised pediatric or drug-specific workflows without separate validation. <br>
Risk: Medication or chemotherapy calculations based on BSA can affect clinical decisions if accepted without review. <br>
Mitigation: Independently verify any medication or chemotherapy dose calculation against authoritative clinical protocols before use. <br>
Risk: The optional output path writes calculation results to a local file. <br>
Mitigation: Choose output paths deliberately and avoid writing patient-identifying information to unsafe locations. <br>


## Reference(s): <br>
- [BMI & BSA Calculator Guidelines](references/guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/bmi-bsa-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, files, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON calculation results, with optional local file output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses weight in kilograms, height in centimeters, and an optional dose per square meter.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
