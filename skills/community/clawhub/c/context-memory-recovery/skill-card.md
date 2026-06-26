## Description: <br>
Use when a user asks an OpenClaw, Hermes, or similar file-backed agent to preserve, recover, checkpoint, or restore working context across new sessions, model changes, compaction, account switches, restarts, crashes, or memory loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremymartinus-pixel](https://clawhub.ai/user/jeremymartinus-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give file-backed agents a structured recovery protocol for preserving task state, decisions, blockers, preferences, and next actions across session or model changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace recovery notes may capture sensitive project context or personal data if used carelessly. <br>
Mitigation: Review generated memory files periodically and avoid storing passwords, tokens, private keys, or sensitive personal data. <br>
Risk: Shared or untrusted repositories can expose recovery files to people who should not see private task context. <br>
Mitigation: Use the skill in shared repositories only with consent and keep private memory out of shared chat or repository contexts unless explicitly authorized. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jeremymartinus-pixel/context-memory-recovery) <br>
- [Publisher Profile](https://clawhub.ai/user/jeremymartinus-pixel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown recovery files and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains workspace recovery notes such as SESSION-STATE.md, memory/YYYY-MM-DD.md, and MEMORY.md when the agent has file access.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
