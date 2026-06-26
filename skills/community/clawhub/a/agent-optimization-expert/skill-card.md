## Description: <br>
Agent优化专家 helps diagnose and repair agent execution issues such as cron failures, tool errors, workflow interruptions, performance degradation, and OpenClaw or Hermes environment problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect agent health, diagnose failed cron jobs or tool calls, propose repairs, and maintain operational troubleshooting patterns for OpenClaw and Hermes environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad automated repair and self-update authority. <br>
Mitigation: Require explicit approval and reviewable diffs before enabling recurring checks, repair paths, or weekly self-updates. <br>
Risk: Maintenance actions can include file deletion, Docker pruning, service restarts, and stopping sub-agents. <br>
Mitigation: Treat destructive cleanup, service restarts, and process termination as manual-only actions after previewing impact. <br>
Risk: The first-run smoke test may inspect local system state immediately after installation. <br>
Mitigation: Disable automatic first-run checks unless the operator has approved the health inspection scope. <br>


## Reference(s): <br>
- [Dual Environment Adaptation Guide](references/dual-env-adaptation.md) <br>
- [Anthropic Engineering Practice Patterns](references/anthropic-patterns.md) <br>
- [OpenAI Engineering Practice Patterns](references/openai-patterns.md) <br>
- [Error Taxonomy and Handling Strategy](references/error-taxonomy.md) <br>
- [Fix Templates](references/fix-templates.md) <br>
- [Self-Evolution Workflow](references/self-evolution.md) <br>
- [Trigger Integration](TRIGGER-INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with diagnostic steps, repair recommendations, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include health-check summaries, cron or tool-failure diagnosis, proposed configuration changes, and repair verification notes.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
