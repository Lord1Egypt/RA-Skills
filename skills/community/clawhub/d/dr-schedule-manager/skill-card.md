## Description: <br>
Design and implement reliable scheduled or event-triggered automations for OpenClaw agents so changes to model, prompt, delivery, and policy take effect immediately on the next run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to design or migrate scheduled OpenClaw jobs so each run loads current prompts, policies, model rules, and delivery settings. It is intended for cron jobs, reminders, digests, briefings, background agents, and reusable automation standards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying schedule or delivery changes directly can trigger live notifications, public posts, or production mutations before the behavior is validated. <br>
Mitigation: Use dry-run generation, separate delivery and scheduler tests, and require explicit approval before enabling live sends or production mutations. <br>
Risk: Cron registrations or persistent sessions may preserve stale prompt, model, policy, or delivery details. <br>
Mitigation: Keep the scheduler as a thin trigger and load the manifest, prompt, policy files, model policy, and delivery contract at runtime. <br>
Risk: Outbound delivery can fail or route incorrectly when session metadata does not match the provider-required target format. <br>
Mitigation: Define provider-aware delivery contracts and test final outbound delivery independently from scheduler announce behavior. <br>


## Reference(s): <br>
- [Architecture patterns for reliable scheduled jobs](references/architecture-patterns.md) <br>
- [Migration checklist for stale scheduled jobs](references/migration-checklist.md) <br>
- [Reliability review for scheduled job architecture](references/reliability-review.md) <br>
- [Job manifest template](references/job-manifest-template.json) <br>
- [Example migration: Daily briefing job](references/example-migration-daily-briefing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON manifest examples and checklist-style recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed architecture patterns, manifest structure, verification plans, checkpoint gates, and rollout recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
