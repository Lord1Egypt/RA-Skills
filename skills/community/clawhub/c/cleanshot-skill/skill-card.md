## Description:

Use when the user wants an OpenClaw agent to choose the right CleanShot Tool plugin call for screenshots, OCR, screen recording, scrolling capture, annotation, pinned references, CleanShot history, Quick Access, or settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyzmin41](https://clawhub.ai/user/lyzmin41)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to help an agent choose appropriate CleanShot Tool plugin workflows for screenshots, OCR, screen recording, scrolling capture, annotation, pinned references, history access, display selection, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate CleanShot Tool plugin can capture or record visible screen content.

Mitigation: Install only when comfortable granting that access, and review the screen before sharing captures or recordings.

Risk: CleanShot Cloud upload can create a shareable link for captured content.

Mitigation: Use upload only when the user explicitly requests a CleanShot Cloud link; otherwise prefer local copy or save workflows.

Risk: Multi-monitor or region requests can be inaccurate if display geometry is unknown.

Mitigation: Use `cleanshot_get_displays` when geometry is needed, and fall back to manual area selection instead of inventing coordinates.

Risk: Some CleanShot actions may open UI or require confirmation rather than completing automatically.

Mitigation: Do not claim a screenshot was sent, OCR text was returned, or recording started unless the environment or CleanShot confirms that result.

## Reference(s):

- [CleanShot Skill release page](https://clawhub.ai/lyzmin41/skills/cleanshot-skill)
- [Publisher profile](https://clawhub.ai/user/lyzmin41)
- [README](README.md)
- [Examples](examples.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown guidance with CleanShot tool names, modes, actions, and parameter recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; requires the separate CleanShot Tool plugin, macOS, CleanShot X, and CleanShot X API access.]

## Skill Version(s):

0.2.0 (source: package.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
