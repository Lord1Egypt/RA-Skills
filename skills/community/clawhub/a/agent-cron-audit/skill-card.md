## Description: <br>
Agent Cron Audit provides a read-only health audit for recurring and scheduled AI agent jobs, finding silent failures, duplicate active jobs, retry loops, over-frequent schedules, stale automations, risky model usage, and context bloat with evidence-first manual verification before any change. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choosenobody](https://clawhub.ai/user/choosenobody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect recurring or scheduled AI agent jobs for health risks before changing job schedules, prompts, models, or configuration. The audit is evidence-first and read-only, with manual verification before any action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may inspect scheduled job definitions, run history, and outputs that contain sensitive operational details. <br>
Mitigation: Keep inspection local and share only redacted evidence when asking for outside help. <br>
Risk: Findings could be mistaken for instructions to change or disable jobs before they are verified. <br>
Mitigation: Review findings manually before changing any job, and treat the skill output as evidence and guidance rather than an automatic fix. <br>


## Reference(s): <br>
- [Agent Cron Audit on ClawHub](https://clawhub.ai/choosenobody/agent-cron-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown audit sections with redacted evidence and a manual verification prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output; no auto-fix, telemetry, external LLM call, or network call behavior found in the security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
