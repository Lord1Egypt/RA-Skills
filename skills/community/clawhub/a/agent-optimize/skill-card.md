## Description:

Agent Optimize diagnoses OpenClaw context bloat, skill noise, memory redundancy, and configuration conflicts, then produces optimization reports and suggested cleanup actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chungvic](https://clawhub.ai/user/chungvic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit OpenClaw workspaces for slowdowns caused by large session history, noisy or duplicate skills, memory growth, and conflicting configuration. It returns health metrics and suggested cleanup actions for review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session files, memory metadata, skill folders, configuration files, and workspace environment files, so generated reports may contain sensitive local information.

Mitigation: Review reports before sharing, store backups and reports in protected locations, and treat diagnostic output as potentially sensitive.

Risk: Documentation describes cleanup, backup, cron, and auto-fix workflows that can affect local sessions, memory, skills, or configuration.

Mitigation: Keep auto-fix disabled by default, review proposed commands before execution, and maintain a restorable backup before cleanup or scheduled automation.

Risk: Security evidence flags the release as suspicious because its behavior extends beyond a simple read-only diagnostic posture.

Mitigation: Install only after reviewing the requested permissions and prefer a revised release that clearly separates read-only diagnostics from write-capable cleanup.

## Reference(s):

- [Agent Optimize ClawHub release page](https://clawhub.ai/chungvic/skills/agent-optimize)
- [OpenClaw Performance Optimization Guide](https://docs.openclaw.ai/performance)
- [OpenClaw Context Management Best Practices](https://docs.openclaw.ai/context-management)
- [OpenClaw Skill Optimization Guide](https://docs.openclaw.ai/skill-optimization)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown, JSON, or Feishu card diagnostic reports with optimization recommendations and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include local file paths, workspace metrics, and cleanup recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata, README.md, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
