## Description: <br>
Fitbit data connector skill for OpenClaw. Exposes compact auth/fetch/store/quality tools; OpenClaw performs all coaching reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaodriessen](https://clawhub.ai/user/joaodriessen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to authenticate with Fitbit, fetch or sync recent Fitbit and unified health metrics, and return compact JSON for downstream reasoning. It is intended for data retrieval and quality checks, not medical diagnosis or coaching decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The published package includes real-looking Fitbit OAuth token backups and private calendar/log artifacts. <br>
Mitigation: Do not install this release publicly; revoke or rotate exposed credentials, remove private backups and logs, and republish a sanitized package. <br>
Risk: The connector handles sensitive health data across Fitbit, Apple Health import, calendar ingestion, local caches, and backups. <br>
Mitigation: Use explicit scoping, least-privilege OAuth grants, local-only storage, and documented retention/pruning before broad distribution. <br>
Risk: Health metrics can be mistaken for medical or coaching advice if the output is used beyond the skill's data-plane role. <br>
Mitigation: Use the skill only to retrieve and quality-check data; keep diagnosis, coaching, and training decisions in reviewed downstream workflows. <br>


## Reference(s): <br>
- [Fitbit Capability Matrix](references/CAPABILITY_MATRIX.md) <br>
- [Fitbit Capability Contract](references/capability_contract.json) <br>
- [Fitbit Training Schema](references/schema.md) <br>
- [Fitbit Web API Swagger](https://dev.fitbit.com/build/reference/web-api/explore/fitbit-web-api-swagger.json) <br>
- [Fitbit Authorization Guide](https://dev.fitbit.com/build/reference/web-api/developer-guide/authorization/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Compact JSON with Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Use narrow metric selections where possible; local SQLite cache improves reliability while Fitbit remains the source of truth.] <br>

## Skill Version(s): <br>
1.0.0 (source: _meta.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
