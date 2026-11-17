## Description:

Top-level cross-platform computer-use skill that bundles standalone macOS, Windows, and Linux runtimes with zero local Claude dependency and selects the correct platform payload at install/use time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to install, build, and run a portable computer-use runtime across macOS, Windows, and Linux. It supports desktop automation workflows through platform-specific MCP server payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables screen viewing, app control, keyboard and mouse input, and clipboard access on the local desktop.

Mitigation: Use only on trusted, isolated desktops and close sensitive apps before running desktop automation workflows.

Risk: The security evidence reports powerful desktop access without the separate user approval its tooling describes.

Mitigation: Review actions before execution and require a real approval or allowlist flow before finance, admin, secrets, or personal-account workflows.

Risk: Runtime validation differs by platform: macOS is real-device validated, while Windows and Linux still need end-to-end validation on real hosts.

Mitigation: State the active host platform and validation status before treating behavior as verified.

Risk: Linux desktop control targets X11 first, and Wayland may restrict screenshots, focus inspection, clipboard, and synthetic input.

Mitigation: Validate the desktop environment and permission model on the target Linux host before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wimi321/skills/cross-platform-computer-use-skill)
- [macOS Computer-Use Skill](https://clawhub.ai/wimi321/computer-use-macos)
- [Windows Computer-Use Skill](https://clawhub.ai/wimi321/computer-use-windows)
- [Linux Computer-Use Skill](https://clawhub.ai/wimi321/computer-use-linux)
- [macOS runtime repository](https://github.com/wimi321/macos-computer-use-skill)
- [Windows runtime repository](https://github.com/wimi321/windows-computer-use-skill)
- [Linux runtime repository](https://github.com/wimi321/linux-computer-use-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects one platform payload for the current host and reports platform-specific validation limits.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
