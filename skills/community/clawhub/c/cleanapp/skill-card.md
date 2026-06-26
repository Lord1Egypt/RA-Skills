## Description: <br>
Submits problem reports such as bugs, incidents, hazards, scams, UX friction, policy violations, and improvement proposals to CleanApp through its quarantine-first Fetcher Key System. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[borisolver](https://clawhub.ai/user/borisolver) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to submit structured issue reports to CleanApp, either in bulk from JSON or as single manual reports. It is suited for report intake workflows that need dry-run checks, idempotency keys, and optional location or media minimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Report submissions are sent to an external CleanApp service and may include sensitive report text, optional location, or optional media metadata. <br>
Mitigation: Run with --dry-run before sending, use --approx-location or --no-location for location minimization, and use --no-media unless media metadata is necessary. <br>
Risk: The skill requires a CleanApp API token for live submissions. <br>
Mitigation: Store CLEANAPP_API_TOKEN through the platform secret manager and revoke or rotate the token if it is exposed. <br>
Risk: Retries or repeated agent actions can submit duplicate or unwanted reports if source identifiers are not managed carefully. <br>
Mitigation: Provide stable source_id values for bulk submissions and review dry-run payloads before live execution. <br>


## Reference(s): <br>
- [CleanApp Skill Page](https://clawhub.ai/borisolver/cleanapp) <br>
- [CleanApp Ingest API Reference](references/API_REFERENCE.md) <br>
- [CleanApp Swagger UI](https://live.cleanapp.io/v1/docs) <br>
- [CleanApp OpenAPI YAML](https://live.cleanapp.io/v1/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, and command output from report submission or dry-run execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces report-submission instructions and may execute helper scripts that print dry-run payloads or CleanApp API responses.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
