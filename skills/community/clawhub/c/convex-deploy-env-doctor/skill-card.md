## Description:

Validate and fix Convex deployment configuration for skills/apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okikesolutions](https://clawhub.ai/user/okikesolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug Convex deployment URL, callback, environment variable, and backend connectivity issues before publishing or deploying a skill or app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect environment files that contain secrets.

Mitigation: Inspect only needed Convex-related environment keys and redact values in all outputs.

Risk: Connectivity checks may contact configured backend URLs.

Mitigation: Contact only HTTPS backend URLs the user recognizes or controls, and disclose external endpoints touched.

## Reference(s):

- [Convex Env Doctor Output Template](artifact/references/output-template.md)
- [ClawHub Skill Page](https://clawhub.ai/okikesolutions/skills/convex-deploy-env-doctor)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with pass/fail findings, file-level evidence, required fixes, data-routing disclosure, and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secrets must be redacted; failing checks include file and line evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
