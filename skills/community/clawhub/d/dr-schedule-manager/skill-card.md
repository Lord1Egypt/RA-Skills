## Description: <br>
Design and implement reliable scheduled or event-triggered automations for OpenClaw agents so changes to model, prompt, delivery, and policy take effect immediately on the next run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, review, and migrate scheduled automations so each run loads current manifests, prompts, policy, model selection, and delivery configuration. It is intended for cron jobs, briefings, reminders, digests, monitors, and background agent workflows that must avoid stale scheduler payloads or session state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated job manifests or scheduler entries may enable live sends, public posts, production writes, or customer-facing schedule changes before they have been reviewed. <br>
Mitigation: Review each generated manifest and scheduler entry, keep delivery targets explicit, and require approval before enabling live delivery or production mutations. <br>
Risk: Scheduled automations can keep using stale prompts, policies, model choices, delivery routes, or session state if runtime inputs are embedded in scheduler payloads. <br>
Mitigation: Use thin scheduler references and make each run load current manifest, prompt, policy, model, and delivery files at runtime; verify the registered scheduler payload and selected execution substrate. <br>
Risk: Deterministic high-frequency jobs may unnecessarily consume LLM tokens or introduce model latency if routed through an agent runner. <br>
Mitigation: Use a non-agent runner for deterministic jobs unless a written justification shows that runtime reasoning or natural-language generation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniel-refahi-ikara/skills/dr-schedule-manager) <br>
- [Architecture patterns for reliable scheduled jobs](references/architecture-patterns.md) <br>
- [Migration checklist for stale scheduled jobs](references/migration-checklist.md) <br>
- [Reliability review for scheduled job architecture](references/reliability-review.md) <br>
- [Job manifest template](references/job-manifest-template.json) <br>
- [Example migration: Daily briefing job](references/example-migration-daily-briefing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and optional shell command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include manifest structures, execution substrate recommendations, migration steps, verification plans, checkpoint gates, and reliability tradeoffs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
