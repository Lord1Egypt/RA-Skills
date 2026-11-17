## Description:

Use this skill whenever connecting a patient's real health records from EHR systems (Epic, Cerner, Athena) or the TEFCA national network into HealthClaw Guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aks129](https://clawhub.ai/user/aks129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect patient-authorized EHR and TEFCA records into HealthClaw Guardrails, monitor ingestion jobs, configure Fasten webhooks, and run post-import Curatr quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports workflows involving real patient data and health-record exports.

Mitigation: Review before installing in patient-data environments, test with synthetic patients first, and confirm authentication, consent, and tenant isolation controls before live use.

Risk: Credential examples may encourage private keys in shell commands or local environment handling.

Mitigation: Use secret-managed credentials and keep Fasten private keys server-side only.

Risk: Large EHI exports and expiring download links can fail if hosted on short-lived serverless infrastructure.

Mitigation: Use persistent server deployments for production ingestion and monitor job status so failed or interrupted downloads can be retriggered.

## Reference(s):

- [Fasten Connect documentation](https://docs.connect.fastenhealth.com)
- [Fasten Developer Portal](https://app.connect.fastenhealth.com)
- [Fasten EHI export API](https://api.connect.fastenhealth.com/v1/bridge/fhir/ehi-export)
- [Fasten webhook debugging simulator](https://docs.connect.fastenhealth.com/guides/webhook-debugging-simulator.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline HTML, JavaScript, bash, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for Fasten Connect setup, webhook handling, EHI export monitoring, and HealthClaw ingestion workflows.]

## Skill Version(s):

1.6.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
