## Description:

Configure Cross-Origin Resource Sharing correctly to avoid security issues and debugging pain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a concise CORS reference for configuring browser cross-origin requests, credentials, origin allowlists, caching headers, exposed headers, and preflight behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect CORS origin, credential, or caching configuration can expose sensitive responses or break browser clients.

Mitigation: Validate exact origin allowlists, avoid wildcard credentials with credentials mode, include appropriate Vary headers, and test preflight behavior in the target application.

Risk: CORS controls do not replace authentication or CSRF protections for sensitive endpoints.

Mitigation: Require application authentication and CSRF protections in addition to CORS response headers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/cors)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown reference guidance with inline configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reference guidance only; no files, commands, credentials, or network access are requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
