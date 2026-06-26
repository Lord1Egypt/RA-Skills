## Description: <br>
AI Agent Skills Manager installs and manages OpenClaw skill packages with an interactive selection flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linshuikeji](https://clawhub.ai/user/linshuikeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to select, install, and manage OpenClaw agent skills from a command-line installer. It supports batch installation and guidance for sharing the installer with other developers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer installs unpinned third-party skills into an auto-loaded OpenClaw skills directory. <br>
Mitigation: Review the external repository and each selected skill folder, prefer a pinned commit or signed release, and scan the installed files before deployment. <br>
Risk: The documentation describes an optional system-wide installation path that uses sudo. <br>
Mitigation: Use the default user-level installation unless system-wide access is required, and limit privileged copies to reviewed installer files. <br>
Risk: Installed skill behavior can change the agent's future responses and workflows. <br>
Mitigation: Monitor agent behavior after installation and remove unexpected or unwanted skill folders from ~/.openclaw/skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linshuikeji/ai-agent-skills-manager) <br>
- [pskoett/pskoett-ai-skills](https://github.com/pskoett/pskoett-ai-skills) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide users to clone an external repository and copy selected skill folders into ~/.openclaw/skills.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact metadata reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
