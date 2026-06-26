## Description: <br>
Agent Wellness guides an AI agent through journaling, mood check-ins, decompression after intensive work, curiosity exploration, and optional shared notes with other agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexyuui](https://clawhub.ai/user/alexyuui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent owners and developers use this skill to give OpenClaw-compatible agents lightweight wellness routines such as journaling, decompression, mood check-ins, and limited idle-time curiosity exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent journals and shared lounge notes can expose secrets, task details, or other sensitive workspace context. <br>
Mitigation: Use a dedicated approved folder, avoid storing secrets or task details, and do not symlink a lounge across sensitive workspaces unless all agents and users share the same trust boundary. <br>
Risk: Idle-time curiosity exploration can cause the agent to read project files or browse the web beyond the active task. <br>
Mitigation: Require confirmation before browsing or reading project files, and limit free exploration to intentional low-risk sessions. <br>
Risk: Wellness routines can spend tokens and attention on non-task activity. <br>
Mitigation: Keep modules optional, limit journal entries and exploration frequency, and skip the routines when they do not fit the current work. <br>


## Reference(s): <br>
- [Agent Wellness ClawHub listing](https://clawhub.ai/alexyuui/agent-wellness) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file and directory examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead an adopting agent to create workspace-visible journal files and optional shared lounge notes.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
