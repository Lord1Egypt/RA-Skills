## Description: <br>
Native local memory for OpenClaw agents: Capture, Cue, Project, Recall, and Consolidate conversations into a private Helix-backed brain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moshik21](https://clawhub.ai/user/moshik21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add persistent local memory, recall, project routing, and consolidation workflows to agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and may reuse personal or project context across sessions. <br>
Mitigation: Install only when persistent local memory is intended, and avoid storing secrets, regulated data, or other sensitive content. <br>
Risk: The setup path includes a remote installer command. <br>
Mitigation: Review the installer before running it and confirm the installed runtime, MCP configuration, and readiness checks match the intended environment. <br>
Risk: Forget behavior is described as soft deletion and proactive recall or notifications may surface stored context later. <br>
Mitigation: Check whether purge controls, automatic recall, intentions, and proactive notifications can be disabled or configured before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/moshik21/engram-brain) <br>
- [Engram homepage](https://github.com/Moshik21/engram) <br>
- [Public OpenClaw installer](https://raw.githubusercontent.com/Moshik21/engram/main/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist and recall local conversation and project context through the Engram server.] <br>

## Skill Version(s): <br>
0.3.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
