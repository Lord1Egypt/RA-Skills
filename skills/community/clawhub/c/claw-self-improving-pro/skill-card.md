## Description: <br>
Claw Self Improving Pro helps an agent reflect on its work, learn from explicit corrections, and organize local memory of preferences, workflows, and project patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to make an assistant review its own work, record explicit user corrections, and maintain local, tiered memory for reusable preferences and project patterns. It is intended for agents that should improve execution quality across sessions while keeping stored memory visible and manageable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local cross-session memory can retain user corrections, preferences, workflows, and project patterns longer than intended. <br>
Mitigation: Review ~/self-improving/ periodically, use the documented forget and export flows, and remove or protect exported memory after a full wipe. <br>
Risk: Sensitive information could be written into memory if the agent or user treats the store as general notes. <br>
Mitigation: Follow the documented boundaries: do not store credentials, financial data, medical details, biometric data, third-party information, location patterns, or access patterns. <br>
Risk: Edits to agent instruction files such as AGENTS.md, SOUL.md, or HEARTBEAT.md can affect future behavior. <br>
Mitigation: Review those edits before deployment and keep execution-improvement memory separate from factual continuity notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/williamwang-wh/claw-self-improving-pro) <br>
- [Publisher profile](https://clawhub.ai/user/williamwang-wh) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](boundaries.md) <br>
- [Learning mechanics](learning.md) <br>
- [Memory operations](operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline file paths and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operating guidance for local memory setup, retrieval, correction logging, reflection, compaction, export, and deletion workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
