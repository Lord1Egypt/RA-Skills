## Description: <br>
Fixes Chinese and Unicode character encoding issues when running AI agents on Windows through POSIX-compatible shells such as Git Bash, MSYS2, WSL, and BusyBox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gkd2323c](https://clawhub.ai/user/gkd2323c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to diagnose and correct garbled Chinese or Unicode output in Windows POSIX shell environments. It provides practical fixes for Python, Windows PowerShell, cmd.exe, and subprocess bridges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports no negative finding but also notes limited artifact-backed verification in the supplied scan telemetry. <br>
Mitigation: Review the bundled skill files before installation, with attention to permissions, credential handling, network calls, persistence, and data mutation. <br>
Risk: The helper script and examples invoke Windows PowerShell and cmd.exe commands to inspect and normalize encoding behavior. <br>
Mitigation: Run the commands only in the intended Windows POSIX shell environment and review command text before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gkd2323c/charset-fix) <br>
- [Publisher profile](https://clawhub.ai/user/gkd2323c) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline Bash, Python, and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-focused troubleshooting and command examples] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
