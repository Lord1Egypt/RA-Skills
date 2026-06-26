## Description: <br>
Organizes agent memory like a dream process by preserving important context, compressing conversation state, and forgetting low-value details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nic-yuan](https://clawhub.ai/user/nic-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to manage long-running conversations by estimating token usage, detecting dense information, compressing context, creating memory snapshots, and tracking decisions. It is intended for agents that need local continuity across tasks or sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and mutate conversation state through local memory, decision, and snapshot files. <br>
Mitigation: Require explicit approval before writing memory or snapshots, and periodically inspect the .dream and .workflow/snapshots directories. <br>
Risk: Context compression and forgetting behavior can remove details that may still be important. <br>
Mitigation: Review compressed summaries before replacing working context, and retain snapshots long enough to recover omitted details. <br>
Risk: The documentation references heartbeat, task, and topic shell helpers that are not included in the submitted artifact. <br>
Mitigation: Do not rely on those helpers unless their source is separately reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub Apollo Dream release page](https://clawhub.ai/nic-yuan/apollo-dream) <br>
- [Publisher profile: nic-yuan](https://clawhub.ai/user/nic-yuan) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, JSON state files, and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory, decision, trigger, and snapshot files when invoked.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
