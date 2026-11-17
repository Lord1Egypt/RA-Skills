## Description:

Diagnose and mitigate ClawHub and ClawDHUB publish failures covering authentication, browser-login, missing dependencies, pending security-scan visibility errors, and wrong profile or skill URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluebirdback](https://clawhub.ai/user/bluebirdback)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to diagnose failed ClawHub publishing workflows, prepare safer publish commands, and verify skill visibility after transient scan or registry states.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may install or run the ClawHub CLI without confirming the package source.

Mitigation: Verify the ClawHub CLI package before installation and avoid elevated privileges unless they are strictly required.

Risk: Login tokens can be exposed if copied into shared shells, logs, or command history.

Mitigation: Treat ClawHub tokens as secrets and prefer secure token handling for headless login.

Risk: Temporary files used by shell helpers may expose account or publish state on shared systems.

Mitigation: Use secure temporary files or shell variables before running the scripts in shared environments.

## Reference(s):

- [ClawHub Publish Error Map](references/error-map.md)
- [ClawHub Publish Doctor skill page](https://clawhub.ai/bluebirdback/skills/clawhub-publish-doctor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise diagnostic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retry-aware publish and inspect commands for the ClawHub CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
