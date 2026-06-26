## Description: <br>
Self-reflection, self-criticism, self-learning, and self-organizing memory help an agent evaluate its own work, catch mistakes, and preserve reusable lessons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philippeliang](https://clawhub.ai/user/philippeliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to give an agent local, cross-session memory for explicit corrections, preferences, workflow lessons, and self-reflections. It is intended for improving execution quality over time while keeping memory transparent, scoped, and reviewable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists local, cross-session memory about preferences, corrections, and workflow lessons. <br>
Mitigation: Enable it deliberately, periodically inspect ~/self-improving/, and edit or remove stale or unwanted entries. <br>
Risk: Memory entries could accidentally include secrets or sensitive personal data. <br>
Mitigation: Follow the bundled security boundaries: do not store credentials, financial data, medical data, biometric data, location routines, access patterns, or third-party personal information. <br>
Risk: Setup guidance may propose changes to agent configuration files such as AGENTS.md, SOUL.md, or HEARTBEAT.md. <br>
Mitigation: Review proposed configuration changes before applying them and keep existing project guidance intact. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/philippeliang/claw-self-improving) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory operations](artifact/operations.md) <br>
- [Learning mechanics](artifact/learning.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and local memory file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory and configuration guidance for files under ~/self-improving/ and optional agent configuration files.] <br>

## Skill Version(s): <br>
1.2.10 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
