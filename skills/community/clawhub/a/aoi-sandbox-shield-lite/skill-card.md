## Description:

Creates local snapshots of critical OpenClaw workspace and configuration files, validates JSON configuration syntax and required keys, and emits audit-friendly JSON logs without applying changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmonddantesj](https://clawhub.ai/user/edmonddantesj)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations maintainers use this skill to snapshot local OpenClaw configuration state before releases or audits and to check configuration JSON for syntax and required keys. It is useful when teams need a lightweight audit artifact without applying configuration changes or restarting services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The snapshot command can persistently copy sensitive OpenClaw configuration and agent-state files into a local snapshot directory.

Mitigation: Review the target workspace for secrets or private instructions before running snapshots, restrict local access to snapshot directories, and delete retained snapshots when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmonddantesj/skills/aoi-sandbox-shield-lite)
- [Publisher profile](https://clawhub.ai/user/edmonddantesj)
- [GitHub Issues support](https://github.com/edmonddantesj/aoi-skills/issues)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON emitted to stdout, with Markdown command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot output includes file paths, byte counts, SHA-256 hashes, timestamps, and a local snapshot directory when files are present; config validation output includes pass/fail status and missing-key issues.]

## Skill Version(s):

0.1.2 (source: server release metadata, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
