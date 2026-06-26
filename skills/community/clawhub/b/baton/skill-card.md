## Description: <br>
Always-delegating OpenClaw orchestration skill that spawns a compact Planner-Orchestrator first, then minimal specialist subagents with model routing, rate-limit leases, and safety gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[entrebear](https://clawhub.ai/user/entrebear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use Baton to coordinate subagents for planning, model routing, rate-limit-aware execution, and safety-gated task delegation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baton can coordinate subagents and change local model-routing policy files. <br>
Mitigation: Use explicit wording for model policy changes and review .openclaw/baton changes before committing or deploying them. <br>
Risk: Delegated agents could attempt external, destructive, credential, billing, or production actions if over-authorized. <br>
Mitigation: Keep confirmation enabled and require explicit authorization plus validation before irreversible or high-impact actions. <br>
Risk: Model selection or rate-limit configuration can route work to unintended models or overload a provider. <br>
Mitigation: Maintain a reviewed Baton model allowlist and rate-limit policy before enabling explicit routing in a real workspace. <br>


## Reference(s): <br>
- [Baton ClawHub Page](https://clawhub.ai/entrebear/baton) <br>
- [Planner-Orchestrator protocol](references/planner-orchestration.md) <br>
- [Baton model routing](references/model-routing.md) <br>
- [Baton model discovery and user selection](references/model-discovery.md) <br>
- [Baton model management](references/model-management.md) <br>
- [Baton rate-limit and load-spreading policy](references/rate-limits.md) <br>
- [Baton permission matrix](references/permission-matrix.md) <br>
- [Baton task and run schemas](references/task-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON contracts and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local Baton state under .openclaw/baton when setup, model-management, or routing scripts are run.] <br>

## Skill Version(s): <br>
1.8.2 (source: SKILL.md frontmatter, CHANGELOG.md, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
