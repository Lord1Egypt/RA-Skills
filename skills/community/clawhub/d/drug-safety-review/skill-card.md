## Description: <br>
Comprehensive medication safety review system providing real-time analysis of drug-drug interactions, contraindications, allergy risks, and dosing optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Andyxcg](https://clawhub.ai/user/Andyxcg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare providers, pharmacists, patients, and developers use this skill to review medication lists for drug interactions, contraindications, allergy risks, renal dosing concerns, and alternative therapy suggestions. It is a clinical decision-support aid and its results should be verified with authoritative clinical sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medication safety results may be incomplete or unsuitable as a comprehensive medical safety system. <br>
Mitigation: Treat outputs as clinical decision support only and verify medication recommendations with authoritative clinical references and qualified healthcare professionals. <br>
Risk: User identifiers and trial-use records are written locally, and real patient identifiers could create avoidable privacy exposure. <br>
Mitigation: Use pseudonymous user_id values and avoid entering real patient identifiers when running reviews or testing trial behavior. <br>
Risk: Paid use depends on SkillPay billing configuration and a remote billing endpoint. <br>
Mitigation: Review the billing endpoint, credential environment variable names, and payment behavior before enabling paid operation. <br>
Risk: The artifact includes a background self-evolution daemon that repeatedly runs local evolution code. <br>
Mitigation: Do not run auto-evolve-daemon.sh unless the behavior has been reviewed and explicitly accepted for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Andyxcg/drug-safety-review) <br>
- [Drug database reference](references/drug-database.md) <br>
- [Drug interaction criteria](references/interaction-criteria.md) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime review results are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bilingual Chinese and English messages, local trial tracking, optional output-file writing, and SkillPay billing responses after trial use.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
