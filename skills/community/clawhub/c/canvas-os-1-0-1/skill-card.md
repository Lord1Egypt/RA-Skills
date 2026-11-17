## Description:

Canvas OS helps agents build, store, and run rich visual HTML, CSS, and JavaScript apps on the OpenClaw Canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[knightluozichu](https://clawhub.ai/user/knightluozichu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to create, serve, open, update, and close local Canvas apps for dashboards, trackers, quick displays, and other interactive OpenClaw visual workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local web servers can expose files from the served app directory.

Mitigation: Serve only dedicated app directories with trusted contents, avoid sensitive files in app folders, and stop the server when the app is no longer needed.

Risk: Port cleanup can terminate unrelated local processes using the same port.

Mitigation: Use known app-specific ports and inspect the active listener before allowing cleanup or process termination.

Risk: JavaScript injection and Canvas app messages can trigger unintended behavior when app content or data is untrusted.

Mitigation: Use trusted HTML, JavaScript, and data only; review generated code before Canvas evaluation; and validate app-originated messages before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/knightluozichu/skills/canvas-os-1-0-1)
- [Canvas Loading Reference](artifact/CANVAS-LOADING.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Canvas app files and provide commands for OpenClaw Canvas navigation, JavaScript evaluation, and server lifecycle management.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
