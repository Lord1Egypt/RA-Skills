## Description: <br>
Multi-agent orchestration with 5 proven patterns - Work Crew, Supervisor, Pipeline, Council, and Auto-Routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[variable190](https://clawhub.ai/user/variable190) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate OpenClaw sub-agents for parallel research, dynamic delegation, staged content workflows, expert review, and automatic task routing when orchestration is worth the extra cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt injection or unsafe task propagation from user-provided task text. <br>
Mitigation: Keep tasks scoped and explicit, avoid secrets in task text, rely on the documented task sanitization and safety preamble, and review generated outputs before high-impact actions. <br>
Risk: Sensitive details may be exposed through local state or task previews if safe-state behavior is disabled. <br>
Mitigation: Keep ORCHESTRATOR_SAFE_STATE enabled, remove local state files when no longer needed, and only disable safe-state in controlled debugging. <br>
Risk: Multi-agent orchestration can spend substantially more tokens and spawn additional sessions. <br>
Mitigation: Use the skill for high-value orchestration cases and prefer a single agent for simple, deterministic, or low-context tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/variable190/agent-orchestrator-molter) <br>
- [Skill README](artifact/README.md) <br>
- [Skill command reference](artifact/SKILL.md) <br>
- [Security notes](artifact/SECURITY.md) <br>
- [Pipeline examples](artifact/examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, shell commands, and structured text depending on the selected orchestration pattern.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn multiple OpenClaw sessions and use substantially more tokens than a single-agent run; safe-state mode redacts persisted previews by default.] <br>

## Skill Version(s): <br>
1.0.5 (source: SKILL.md frontmatter, CHANGELOG, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
