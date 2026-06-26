## Description: <br>
Provides a Python-based task management system that models task intake, review, resource budgeting, scheduling, ComfyUI execution, monitoring, and audit logging through a Ming court metaphor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fenzyh](https://clawhub.ai/user/fenzyh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, approve, budget, schedule, execute, monitor, and audit task workflows, including image or video generation through a configured ComfyUI endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External workflow execution can submit work to a configured ComfyUI server. <br>
Mitigation: Use only trusted ComfyUI endpoints, restrict network access, and review endpoint configuration before enabling execution. <br>
Risk: A downloaded output path can write outside the intended task folder. <br>
Mitigation: Fix filename containment and sanitize downloaded filenames before running the scheduler unattended. <br>
Risk: Task archives and logs may contain sensitive local workflow data. <br>
Mitigation: Apply access controls, retention limits, and log review for active_tasks and logs directories. <br>
Risk: Bundled workflow defaults may contain unsuitable prompt content. <br>
Mitigation: Replace bundled prompt defaults with neutral, deployment-appropriate workflow prompts before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fenzyh/daming-core) <br>
- [README](README.md) <br>
- [Skill documentation](SKILL.md) <br>
- [JinYiWei monitoring guide](JINYIWEI_GUIDE.md) <br>
- [Hybrid architecture guide](HYBRID_ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, Python snippets, shell commands, JSON, and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local task archives, logs, audit records, and ComfyUI output files when executed by an agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
