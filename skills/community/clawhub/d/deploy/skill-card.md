## Description: <br>
Ship applications reliably with CI/CD, rollback strategies, and zero-downtime deployment patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DevOps engineers, and release owners use this skill to plan safer application deployments, CI/CD pipelines, zero-downtime releases, database migrations, rollback procedures, and post-deploy monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment advice applied directly to production can cause downtime or failed releases when environment-specific tests, health checks, or rollback paths are missing. <br>
Mitigation: Validate proposed deployment steps in CI and staging, require passing health checks, keep previous artifacts available, and confirm the rollback plan before production changes. <br>
Risk: Migration, rollback, or secret-management changes can affect data integrity or expose credentials if treated as generic instructions. <br>
Mitigation: Have a qualified operator review database and secret-management steps, use a secret manager, test migrations on representative data, and prefer backwards-compatible migration sequences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/deploy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown deployment guidance with checklists, operational recommendations, and possible command or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides deployment best practices and does not include executable code or request credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
