## Description: <br>
Top-level cross-platform computer-use skill that bundles standalone macOS, Windows, and Linux runtimes with zero local Claude dependency and selects the correct platform payload at install/use time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use Deskuse to give an agent a portable local desktop-control runtime across macOS, Windows, and Linux. It helps select, build, and run the matching standalone MCP payload for the current host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over the active desktop, including app interaction and clipboard access. <br>
Mitigation: Install only from a trusted publisher, run it in a dedicated account or sandbox where possible, and keep sensitive applications closed while it is active. <br>
Risk: App, clipboard, and system-key permissions may be granted automatically rather than through a clear approval prompt. <br>
Mitigation: Review the skill before installation and confirm that the requested desktop-control behavior is acceptable for the target environment. <br>
Risk: Windows and Linux payloads are implemented and build-validated but are not documented as end-to-end validated on real target hosts. <br>
Mitigation: Validate the selected payload on the actual target operating system before using it for important workflows. <br>
Risk: Linux behavior can be limited by Wayland compositor policies for screenshots, focus inspection, clipboard access, and synthetic input. <br>
Mitigation: Prefer a supported X11 session for Linux use, or test the exact Wayland compositor and permissions before relying on desktop control. <br>


## Reference(s): <br>
- [Deskuse ClawHub Release](https://clawhub.ai/wimi321/deskuse) <br>
- [Top-Level Skill Instructions](artifact/SKILL.md) <br>
- [Platform Manifest](artifact/project/manifest.json) <br>
- [macOS Runtime README](artifact/project/platforms/macos/README.md) <br>
- [Windows Runtime README](artifact/project/platforms/windows/README.md) <br>
- [Linux Runtime README](artifact/project/platforms/linux/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output is platform-specific and depends on the detected host runtime.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
