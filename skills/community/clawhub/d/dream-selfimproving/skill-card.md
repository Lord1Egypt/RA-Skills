## Description: <br>
Dream Selfimproving runs scheduled memory distillation for OpenClaw, generating insights, updating long-term memory, and drafting or retiring skills based on use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run recurring memory reviews, produce dream and daily reports, search long-term memory, and evolve shared skills from observed capability gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain sensitive conversation content. <br>
Mitigation: Keep secrets out of conversations the skill can log and review stored OpenClaw memory before relying on or sharing it. <br>
Risk: Generated or modified skills under ~/SharedSkills may introduce incorrect behavior or unsafe automation. <br>
Mitigation: Inspect and scan generated skills before installing, enabling, or running them. <br>
Risk: Cron-editing and memory-sync workflows can alter local automation or move memory between OpenClaw and Hermes. <br>
Mitigation: Run cron-editing or sync workflows only in trusted local environments and only after reviewing the current cron and memory state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luis1213899/dream-selfimproving) <br>
- [Skill evolution v5.0 reference](references/skill-evolution-v50.md) <br>
- [OpenClaw-Hermes memory sync](references/hermes-openclaw-memory-sync.md) <br>
- [Diagnostic checklist](references/diagnostic-checklist.md) <br>
- [Multi-agent team architecture reference](references/multi-agent-team-architecture.md) <br>
- [OpenClaw multi-agent architecture article](https://mp.weixin.qq.com/s/D33ScqwgpjiwI4PDN3vUaA) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, generated SKILL.md drafts, JSON memory data, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local OpenClaw memory, SharedSkills drafts, reports, and cron-related configuration when explicitly run.] <br>

## Skill Version(s): <br>
5.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
