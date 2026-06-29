## Description: <br>
Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on behavioral triggers, lifecycle journeys, automation governance, and operational safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to plan, audit, and improve email automation workflows, including trigger inventories, QA plans, overlap audits, governance checklists, and journey optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live email sends, contact imports, suppression changes, DNS/authentication changes, and production automation edits can affect customers or compliance-sensitive systems. <br>
Mitigation: Require explicit human approval before execution and keep recommendations separate from live-system actions. <br>
Risk: Incomplete event, consent, suppression, or frequency-cap data can lead to incorrect automation recommendations. <br>
Mitigation: Confirm source material and data freshness before recommending branches, personalization, imports, or production changes. <br>
Risk: Overlapping or stale automations can create duplicate sends, contradictory offers, or contacts that remain enrolled too long. <br>
Mitigation: Audit overlaps, exits, suppression checks, rollback steps, and test contacts before activating or changing journeys. <br>


## Reference(s): <br>
- [Email Automation Skill Operating Checklist](references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with checklists, audits, plans, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates analysis from live-system actions and requires explicit approval before high-risk email automation changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
