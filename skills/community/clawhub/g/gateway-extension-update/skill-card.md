## Description:

Update OpenClaw skills and plugins and inventory extensions after upgrades: force-update ClawHub skills per agent, dry-run plugin updates, handle pins, back up before updating, and check availability via skills list --json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw operators and developers use this skill to inventory and update skills and plugins after upgrades, diagnose extension availability or update failures, and review duplicate directories, ClawHub links, and plugin authorization requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security assessment rates this release suspicious with medium confidence, citing update actions without authorization and deletion of duplicate skill directories beyond the stated scope; its analysis is incomplete because referenced paths were not found in the bundled artifact.

Mitigation: Review the reported update and directory-removal behavior before installing, and treat the assessment as incomplete rather than as a malicious verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoyunlai/skills/gateway-extension-update)
- [ClawHub Link Validity](references/clawhub-link-validity.md)
- [Core Update Failure Triage](references/core-update-failure-triage.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with status summaries, troubleshooting guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Update inventory with blockers and backup paths, plus diagnostic findings when troubleshooting.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
