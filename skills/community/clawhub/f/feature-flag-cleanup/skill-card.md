## Description: <br>
Audits feature flag debt across LaunchDarkly, Unleash, Flagsmith, GrowthBook, Split, and custom systems, then produces stale-flag inventories, risk-ranked cleanup plans, owner-tagged tickets, removal PRs, and rollback playbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and engineering managers use this skill to audit stale feature flags, prioritize safe removals, prepare owner-specific cleanup queues, and plan flag retirement work across codebases and flag services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may need access to repositories, flag-service exports, telemetry, and ticket data to produce useful audits. <br>
Mitigation: Grant only scoped, task-specific access and prefer read-only tokens for inventory and analysis. <br>
Risk: Generated PRs, tickets, provider scripts, cron jobs, memory entries, or flag archive/delete actions can change operational state. <br>
Mitigation: Require human approval before opening PRs, filing tickets, running provider scripts, setting cron jobs, writing memory entries, or deleting or archiving flags. <br>
Risk: Incorrect feature flag removal can break production behavior, especially for permission, billing, auth, kill switch, regulatory, data residency, or encryption toggles. <br>
Mitigation: Use the skill's risk grades, owner sign-off, tests, low-traffic deploy windows, staged migrations, and rollback plans before removing higher-risk flags. <br>
Risk: The release advertises crypto and purchase capability tags that are not needed for normal feature-flag cleanup. <br>
Mitigation: Do not grant unrelated purchase or crypto authority when installing or running this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/feature-flag-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code snippets, shell commands, ticket and PR drafts, CSV-style inventories, and cleanup plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider-specific API commands, rollback plans, owner queues, dashboard outlines, and prevention policies.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
