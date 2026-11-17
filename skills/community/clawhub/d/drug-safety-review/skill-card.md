## Description:

Comprehensive medication safety review system for analyzing drug-drug interactions, contraindications, allergy risks, renal dosing considerations, and alternative therapy suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxcg](https://clawhub.ai/user/andyxcg)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare providers, pharmacists, patients, and healthcare application developers use this skill to produce medication safety review output for drug interactions, contraindications, allergies, renal dosing, and monitoring considerations. It is clinical decision support and should not replace professional pharmacist or physician judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated medication-safety output may be returned as a successful review.

Mitigation: Require an explicit production configuration that disables demo mode, and label or block simulated output before any clinical workflow consumes it.

Risk: Medication-safety recommendations could be incomplete or clinically unsuitable if the drug database coverage or patient data is incomplete.

Mitigation: Validate the database coverage against authoritative clinical sources and require qualified healthcare review before acting on recommendations.

Risk: Local trial and output files may expose user IDs or other health-usage metadata.

Mitigation: Use non-identifying user IDs, restrict filesystem permissions, and protect or delete local trial and output files according to the deployment privacy policy.

Risk: Self-evolution artifacts can change behavior outside the normal review process.

Mitigation: Disable the auto-evolution daemon in production and require code review, security review, and testing for any generated changes before deployment.

## Reference(s):

- [Drug database reference](references/drug-database.md)
- [Drug interaction criteria](references/interaction-criteria.md)
- [ClawHub skill page](https://clawhub.ai/andyxcg/skills/drug-safety-review)
- [Publisher profile](https://clawhub.ai/user/andyxcg)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance]

**Output Format:** [JSON medication safety results plus Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English output; demo mode may return simulated review data.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
