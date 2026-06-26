## Description: <br>
Agent self-healing engine for diagnosing and repairing OpenClaw execution issues such as cron failures, tool errors, workflow interruptions, and performance degradation, with ongoing self-evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw agent operations, diagnose cron, tool, sub-agent, and system-health failures, propose repairs, and record reusable troubleshooting patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad operational repair authority across cron jobs, service restarts, cleanup workflows, and sub-agent management. <br>
Mitigation: Require explicit confirmation before deletion, Docker prune, service restart, cron update, or sub-agent kill actions. <br>
Risk: Weekly self-update workflows can propose changes to reference files or SKILL.md. <br>
Mitigation: Disable or manually approve weekly self-updates, and review every proposed reference or SKILL.md change before enabling it. <br>
Risk: The release is flagged as requiring sensitive credentials and is intended for operational repair workflows. <br>
Mitigation: Install only for OpenClaw operational repair use cases, and review diagnostic commands that inspect credentials, environment variables, or service permissions. <br>


## Reference(s): <br>
- [Dida Agent Optimizer on ClawHub](https://clawhub.ai/tuobadaidai/dida-agent-optimizer) <br>
- [Trigger Integration](TRIGGER-INTEGRATION.md) <br>
- [Anthropic Engineering Practice Patterns](references/anthropic-patterns.md) <br>
- [OpenAI Agent Patterns](references/openai-patterns.md) <br>
- [Error Taxonomy and Handling Strategy](references/error-taxonomy.md) <br>
- [Common Fix Templates](references/fix-templates.md) <br>
- [Self-Evolution Workflow](references/self-evolution.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with diagnostic steps, repair recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose operational changes that require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
