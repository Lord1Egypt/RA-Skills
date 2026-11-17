## Description:

Canvas as an app platform. Build, store, and run rich visual apps on the OpenClaw Canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fraction12](https://clawhub.ai/user/fraction12)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Canvas-OS to build, launch, and update rich HTML/CSS/JS Canvas apps such as dashboards and trackers. The skill guides agents through local Canvas app serving, direct HTML injection, live data updates, and two-way Canvas-to-agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Canvas app serving can expose local files from the served app directory.

Mitigation: Use the skill only with trusted local Canvas apps, review the directory before serving it, and prefer binding local servers to 127.0.0.1.

Risk: Helper scripts can force-stop an unrelated process that owns the selected port.

Mitigation: Check which process is using the port before allowing cleanup, and avoid passing untrusted port values to helper scripts.

Risk: Direct HTML injection and generated page code can run with weak safeguards.

Mitigation: Inject only trusted HTML and data, and review generated JavaScript before running Canvas eval.

Risk: Dashboard and tracker interactions can send text back to the OpenClaw agent through deep links.

Mitigation: Use trusted templates and review or disable Canvas-to-agent actions before opening apps that handle sensitive data.

## Reference(s):

- [Canvas Loading Reference](artifact/CANVAS-LOADING.md)
- [Canvas OS README](artifact/README.md)
- [Canvas-OS ClawHub Page](https://clawhub.ai/fraction12/skills/canvas-os)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local HTML/CSS/JS app files and Canvas helper commands.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
