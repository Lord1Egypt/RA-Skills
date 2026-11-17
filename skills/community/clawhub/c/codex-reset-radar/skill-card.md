## Description:

Monitor Codex usage reset windows from the third-party Codex Reset Radar public JSON feed, detect changes with schema validation and a local baseline, and optionally provide user-authorized OpenClaw chat alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[advnljs](https://clawhub.ai/user/advnljs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to monitor public Codex reset-window and prediction changes, either with a one-off check or with alerts sent to a destination they authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checks require access to a third-party HTTPS public feed, and the scan does not establish whether the host runtime permits that network access.

Mitigation: Confirm that access to the fixed public feed is suitable for the host runtime; treat failed checks as monitor faults rather than reset alerts.

Risk: Notifications are Chinese-only.

Mitigation: Use chat alerts only when Chinese notifications suit the authorized destination and audience.

Risk: The security review was partial, so a benign verdict does not establish that the skill is risk-free.

Mitigation: Review the unresolved coverage and the skill's stated security and operational limits before deployment.

## Reference(s):

- [Validated feed contract](artifact/references/feed-contract.md)
- [Security, cache, and operational limits](artifact/references/security.md)
- [Codex Reset Radar public summary feed](https://codex-reset-radar.pages.dev/current.json)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [A JSON result with an optional notification string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notifications use fixed local Chinese templates; raw feed prose is not included.]

## Skill Version(s):

1.1.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
