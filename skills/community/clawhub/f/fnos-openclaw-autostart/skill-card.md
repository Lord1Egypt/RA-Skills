## Description:

FnOS OpenClaw boot autostart patch with a management-page toggle that modifies the monitor server/index.js and ui/index.html to enable or disable boot startup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lolisaikou](https://clawhub.ai/user/lolisaikou)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw and FnOS operators use this skill to patch an OpenClaw installation so openclaw-gateway can start automatically on boot and be controlled from the management page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directly patches live OpenClaw server and UI files, which can break the service or make rollback unreliable if repeated or partially applied.

Mitigation: Make separate timestamped backups, confirm each insertion point appears exactly once, stop if the patch marker already exists, validate the edited files before restart, and keep a known-good package or backup for recovery.

Risk: FnOS application updates can replace the patched OpenClaw files and remove the autostart behavior.

Mitigation: After updates, check backups and reapply the patch only after rerunning the documented environment and insertion-point checks.

Risk: FnOS or OpenClaw path and bundle-format differences can make the documented commands target the wrong files or fail.

Mitigation: Review and adjust the path variables for the local installation, verify files exist before editing, and inspect the Bun bundle context before applying the injected code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lolisaikou/skills/fnos-openclaw-autostart)
- [Publisher profile](https://clawhub.ai/user/lolisaikou)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, JavaScript, and HTML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces manual patching, verification, restart, toggle, and rollback instructions for a FnOS OpenClaw installation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
