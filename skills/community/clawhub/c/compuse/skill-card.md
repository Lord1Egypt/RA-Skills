## Description: <br>
Top-level cross-platform computer-use skill that bundles standalone macOS, Windows, and Linux runtimes with zero local Claude dependency and selects the correct platform payload at install/use time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, build, and run a portable computer-use MCP runtime across macOS, Windows, and Linux. It is intended for trusted local desktop automation where an agent may need screenshots, keyboard and mouse input, app launch, window inspection, or clipboard operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides high-privilege desktop control and can see unredacted screens, use keyboard and mouse input, access clipboard content when requested, and launch approved applications. <br>
Mitigation: Install only on trusted local hosts, review intended actions before execution, and avoid using it around sensitive desktop content unless that exposure is acceptable. <br>
Risk: Server security evidence says the standalone permission flow auto-approves high-impact computer-use permissions even though tool text says the user will review them. <br>
Mitigation: Treat permission prompts as advisory, rely on MCP-layer action gating, and require a human review of requested app access and flags before operational use. <br>
Risk: Windows and Linux payloads are implemented and build-validated but still need end-to-end runtime validation on real hosts; Linux also targets X11 first and may be restricted under Wayland. <br>
Mitigation: Validate the selected platform runtime on the target host before relying on it, with special checks for focus, clipboard, screenshots, synthetic input, privilege boundaries, and multi-monitor behavior. <br>


## Reference(s): <br>
- [Compuse ClawHub release](https://clawhub.ai/wimi321/compuse) <br>
- [macOS computer-use skill](https://clawhub.ai/wimi321/computer-use-macos) <br>
- [Windows computer-use skill](https://clawhub.ai/wimi321/computer-use-windows) <br>
- [Linux computer-use skill](https://clawhub.ai/wimi321/computer-use-linux) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces platform-aware install, build, run, validation, and risk guidance for local desktop-control runtimes.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
