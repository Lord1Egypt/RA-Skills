## Description:

Syncs OpenClaw workspace state between machines via Git for migration, backup, status checks, pushes, pulls, and branch sync workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to move or synchronize an OpenClaw workspace across local and remote machines while preserving memory, personality, skills, and configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync workflow can upload private OpenClaw memory, logs, skills, and configuration to a Git remote too broadly.

Mitigation: Use only a private, access-controlled Git remote, add a strict `.gitignore` or allowlist before first push, and inspect staged files before every upload.

Risk: Automated pushes can upload workspace data without a deliberate review step.

Mitigation: Avoid the cron auto-push example unless automatic upload of private workspace data is acceptable.

Risk: Secrets pushed to Git may remain in repository history after deletion.

Mitigation: Rotate exposed secrets and clean Git history if sensitive data is pushed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reed1898/skills/claw-roam)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and bundled Bash script behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script emits terminal status text and runs Git commands against the OpenClaw workspace.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
