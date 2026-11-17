## Description:

Capability Decay Watchdog monitors local skill learned_patterns.json files for success-rate drops and stale activity, then reports alerts with recommended repair, learner-injection, or regression actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local health checks across a skill directory, detect decayed or stale skills, and convert alerts into repair, learner-injection, or regression actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog scans local learned_patterns.json files, which may contain notes, preferences, or other local activity data.

Mitigation: Run it only against intended skill roots and avoid storing secrets or sensitive data in learned_patterns.json fields.

Risk: Health findings depend on learner activity logs and may miss logic regressions in skills that do not record learner data or record it incorrectly.

Mitigation: Pair watchdog results with regression tests or manual review before repair, rollback, or deployment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/capability-decay-watchdog)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON watchdog reports with alert reasons and suggested actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local filesystem scan of learned_patterns.json under the configured skills root]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
