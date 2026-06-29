## Description: <br>
Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on inbox placement, authentication, sender reputation, complaint control, and remediation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and email program owners use this skill to plan, audit, and improve deliverability workflows involving inbox placement, authentication, sender reputation, complaints, bounces, warmup, blocklists, and remediation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations could affect live email systems, sender reputation, or customer contact handling if executed without review. <br>
Mitigation: Require explicit human approval before live sends, DNS/authentication edits, contact imports, suppression changes, provider migrations, production automation changes, or destructive cleanup. <br>
Risk: Incomplete evidence about consent, suppression state, complaint rates, bounces, or provider-specific patterns could lead to misleading deliverability conclusions. <br>
Mitigation: Collect evidence by domain, provider, segment, campaign, and time window, and do not assume missing fields, consent, or suppression state. <br>
Risk: Warmup, remediation, or reputation recovery work can worsen deliverability if it lacks stop criteria. <br>
Mitigation: Use staged remediation plans with stop-loss thresholds, monitoring cadence, and an owner for each action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polnikale/emaildeliverabilityskill) <br>
- [Publisher profile](https://clawhub.ai/user/polnikale) <br>
- [Email Deliverability Skill Operating Checklist](references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown recommendations, audits, checklists, runbooks, schedules, configuration guidance, code, and shell commands when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates recommendations from live-system actions and requires explicit approval before high-risk email, DNS, contact, suppression, migration, automation, or cleanup changes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
