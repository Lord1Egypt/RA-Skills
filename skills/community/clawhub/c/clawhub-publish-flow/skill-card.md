## Description:

Publish or update OpenClaw skills on ClawHub through an authenticated local session, including version checks, payload review, direct API upload, and post-release verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-hanasq](https://clawhub.ai/user/g-hanasq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use this skill to publish reviewed local skill folders to ClawHub, choose versions and changelogs, inspect remote state, upload through the bundled Node script, and verify the final release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles bearer-token authenticated uploads and public release payloads with limited built-in scoping or confirmation.

Mitigation: Inspect the exact outbound package, remove secrets and local-only files, verify the registry is the intended HTTPS ClawHub endpoint, and run the upload only for trusted releases.

Risk: Publishing can expose local skill files publicly or update an existing remote skill version.

Mitigation: Review the skill before publishing, inspect the current remote version, choose an explicit target version and changelog, and verify the result with ClawHub after upload.

## Reference(s):

- [Release Checklist](references/release-checklist.md)
- [ClawHub skill page](https://clawhub.ai/g-hanasq/skills/clawhub-publish-flow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Operational Markdown with command examples and release status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include upload commands, verification results, risks, and follow-up notes.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
