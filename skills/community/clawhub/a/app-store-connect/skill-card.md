## Description:

Manage iOS apps, TestFlight builds, submissions, and analytics via App Store Connect API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and app release teams use this skill to guide App Store Connect API authentication, build processing checks, TestFlight distribution, App Review submission, metadata updates, and analytics retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apple API credentials and generated JWTs could be exposed through source control, shared terminals, or logs.

Mitigation: Use least-privileged Apple API keys, keep the .p8 private key out of source control, and avoid exposing generated JWTs in shared terminals or logs.

Risk: POST or PATCH requests can change app metadata, testers, bundle IDs, submissions, releases, or reports.

Mitigation: Review any proposed write request before execution and confirm the target app, version, team, and payload.

## Reference(s):

- [App Store Connect skill page](https://clawhub.ai/ivangdavila/skills/app-store-connect)
- [Skill homepage](https://clawic.com/skills/app-store-connect)
- [API Authentication](artifact/api-auth.md)
- [Common Workflows](artifact/workflows.md)
- [App Store Connect](https://appstoreconnect.apple.com)
- [App Store Connect API apps endpoint](https://api.appstoreconnect.apple.com/v1/apps)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses App Store Connect API credentials from ASC_ISSUER_ID, ASC_KEY_ID, and ASC_PRIVATE_KEY_PATH.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
