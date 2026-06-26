## Description: <br>
Stop your AI agent from forgetting everything between sessions with a file-based memory workspace, session handoff, daily logs, owner namespace templates, and a setup script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to initialize a persistent Markdown memory structure that an AI agent can read and maintain across sessions. It is intended for file-based agents that need continuity, user preferences, project context, and handoff notes in a workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace memory files are plaintext and may contain personal, project, or relationship context. <br>
Mitigation: Use the skill only where plaintext persistent memory is acceptable, avoid storing secrets or regulated data, and add memory files to .gitignore when the workspace is version controlled. <br>
Risk: Agents may load broader personal or relationship context than a task requires. <br>
Mitigation: Keep owner namespace files focused, load sensitive files only when relevant, and periodically review and prune memory content. <br>
Risk: Parallel sessions can update local memory files out of order. <br>
Mitigation: Use this memory structure for one primary agent session per workspace or manually reconcile memory files after concurrent work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/agent-memory-sr) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README](artifact/README.md) <br>
- [QUICKSTART](artifact/QUICKSTART.md) <br>
- [LIMITATIONS](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates plaintext Markdown memory files in the selected workspace; no external dependencies are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
