## Description:

Checks multiple medications for drug-drug interactions and reports severity, mechanisms, effects, warnings, and management guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, clinicians, pharmacists, and developers can use this skill to screen medication lists for known drug-drug interactions and receive severity-ranked educational guidance. Medication decisions should be verified with a licensed clinician or pharmacist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable medication guidance from a limited local database and does not account for patient-specific factors.

Mitigation: Use it only as an educational screening aid and verify every medication decision with a pharmacist or clinician.

Risk: The documented dependency install introduces avoidable install-time risk.

Mitigation: Install only in an isolated environment and avoid the documented dependency install unless the package is revised to remove or pin unnecessary requirements.

Risk: Documented output options differ from the implemented command-line options.

Mitigation: Validate the desired output mode before operational use and rely on supported text or JSON output unless the package is updated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/drug-interaction-checker)
- [Drug Interaction Database](artifact/references/interactions_db.json)
- [Severity Classification Criteria](artifact/references/severity_criteria.md)
- [CYP450 Substrate Data](artifact/references/cyp450_substrates.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON command output with severity summaries, interaction details, warnings, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script exits with nonzero status when major or critical interactions are detected.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; skill frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
