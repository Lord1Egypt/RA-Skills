## Description: <br>
Agent Optimize analyzes OpenClaw context, skill, memory, configuration, and system state to identify performance bottlenecks and generate optimization reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose context bloat, skill noise, memory redundancy, configuration conflicts, and local resource issues, then produce optimization recommendations and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive local OpenClaw state such as sessions, memory files, paths, and configuration details. <br>
Mitigation: Run it manually in report-only mode first and review the generated report before acting on recommendations. <br>
Risk: Auto-fix and scheduled cron examples may modify local agent state if enabled without inspection. <br>
Mitigation: Inspect the exact commands and keep OPTIMIZE_AUTO_FIX disabled until the intended changes and backups are confirmed. <br>
Risk: Generated reports and temporary backups may expose session, memory, path, or configuration details. <br>
Mitigation: Avoid sharing reports or /tmp backups externally and remove sensitive artifacts after review. <br>


## Reference(s): <br>
- [Agent Optimize on ClawHub](https://clawhub.ai/chungvic/agent-optimize) <br>
- [OpenClaw Performance Optimization Guide](https://docs.openclaw.ai/performance) <br>
- [OpenClaw Context Management Best Practices](https://docs.openclaw.ai/context-management) <br>
- [OpenClaw Skill Optimization Guide](https://docs.openclaw.ai/skill-optimization) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or JSON diagnostic report with recommendations; optional Feishu card output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report-only by default; auto-fix behavior is opt-in through OPTIMIZE_AUTO_FIX and may suggest or execute local cleanup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
