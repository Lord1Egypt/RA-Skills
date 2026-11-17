## Description:

Top-level cross-platform computer-use skill that bundles standalone macOS, Windows, and Linux runtimes with zero local Claude dependency and selects the correct platform payload at install/use time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an agent local desktop-control capabilities across macOS, Windows, and Linux through the matching bundled runtime and MCP server. It is intended for trusted-local workflows where screenshots, mouse and keyboard control, app launch, window inspection, display mapping, and clipboard access are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants a local agent broad desktop-control authority, including screenshots, mouse and keyboard actions, app launch, window inspection, display mapping, and clipboard access.

Mitigation: Use only on trusted local machines, close sensitive windows, clear or protect sensitive clipboard contents, and review action permission requests before allowing execution.

Risk: The runtime can bootstrap mutable Node and Python dependencies on first use.

Mitigation: Prefer pinned and hash-verified dependency releases before use on real workstations, and review dependency changes during upgrades.

Risk: Windows and Linux runtime behavior is implemented and build-validated but not end-to-end validated on real hosts in the submitted artifact evidence.

Mitigation: Perform real-host validation for Windows and Linux, including permission boundaries, focus behavior, clipboard access, screenshots, and multi-monitor or compositor-specific edge cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wimi321/skills/deskuse)
- [macOS Computer-Use Skill](https://clawhub.ai/wimi321/computer-use-macos)
- [Windows Computer-Use Skill](https://clawhub.ai/wimi321/computer-use-windows)
- [Linux Computer-Use Skill](https://clawhub.ai/wimi321/computer-use-linux)
- [macOS platform repository](https://github.com/wimi321/macos-computer-use-skill)
- [Windows platform repository](https://github.com/wimi321/windows-computer-use-skill)
- [Linux platform repository](https://github.com/wimi321/linux-computer-use-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are platform-aware and should state the current host platform and validation status when relevant.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
