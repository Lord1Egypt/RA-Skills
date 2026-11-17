## Description:

Curatr helps patients and their agents evaluate FHIR R4 US Core health records for coding and structural issues, explain findings in plain language, apply patient-approved fixes with Provenance records, or prepare provider correction requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aks129](https://clawhub.ai/user/aks129)

### License/Terms of Use:

MIT-0

## Use Case:

Patients, caregivers, and health application developers use Curatr to review FHIR health-record resources for outdated code systems, invalid terminology, missing fields, and display-name mismatches. The skill supports patient-controlled correction workflows by requiring approval before changes and by producing Provenance-backed updates or provider-facing correction summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup and the HealthClaw stack source need review before installation.

Mitigation: Verify the stack source and pin or lock the npm and Python dependencies before deploying the skill.

Risk: The STEP_UP_SECRET protects write operations and could authorize changes if exposed.

Mitigation: Keep STEP_UP_SECRET scoped to the runtime that needs it and rotate it if exposure is suspected.

Risk: Resource coverage may be limited, especially for non-Condition resources and cases where public terminology services are unavailable.

Mitigation: Treat non-Condition checks as limited, review results before acting, and confirm important terminology findings against authoritative sources when live lookups fail.

Risk: Applying fixes changes the patient-facing FHIR record and could introduce incorrect clinical data if unreviewed.

Mitigation: Use only patient-approved fixes, require step-up plus human confirmation for writes, and rely on generated Provenance records for auditability.

## Reference(s):

- [Curatr ClawHub listing](https://clawhub.ai/aks129/skills/curatr)
- [Publisher profile](https://clawhub.ai/user/aks129)
- [HL7 public FHIR terminology server](https://tx.fhir.org)
- [NLM Clinical Tables API](https://clinicaltables.nlm.nih.gov)
- [RxNav API](https://rxnav.nlm.nih.gov)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured MCP tool inputs or outputs, including JSON examples and shell setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evaluation output includes issue severity, field path, plain-language impact, and suggested fixes; write actions require step-up and human confirmation.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
