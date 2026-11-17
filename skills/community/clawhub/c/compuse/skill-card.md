## Description:

Top-level cross-platform computer-use skill that bundles standalone macOS, Windows, and Linux runtimes with zero local Claude dependency and selects the correct platform payload at install/use time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an agent portable desktop-control capability through a bundled MCP runtime on macOS, Windows, or Linux. It is intended for trusted-local computer-use sessions where the agent may inspect screenshots, use the keyboard and mouse, launch apps, and interact with the clipboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant broad local desktop-control access.

Mitigation: Use it only in trusted-local sessions and keep sensitive windows, files, and clipboard contents away from the agent session.

Risk: The security summary reports unfiltered screenshots.

Mitigation: Assume visible screen content may be exposed to the agent and avoid running the skill alongside sensitive applications.

Risk: The security guidance says the build needs review until request_access requires real user approval and Python dependencies are pinned and hash-verified.

Mitigation: Review approval behavior and dependency pinning before higher-trust or unattended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wimi321/skills/compuse)
- [macOS platform ClawHub release](https://clawhub.ai/wimi321/computer-use-macos)
- [Windows platform ClawHub release](https://clawhub.ai/wimi321/computer-use-windows)
- [Linux platform ClawHub release](https://clawhub.ai/wimi321/computer-use-linux)
- [macOS platform repository](https://github.com/wimi321/macos-computer-use-skill)
- [Windows platform repository](https://github.com/wimi321/windows-computer-use-skill)
- [Linux platform repository](https://github.com/wimi321/linux-computer-use-skill)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide platform selection, build, run, and MCP configuration for the bundled runtime.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
