## Description:

Survival protocol for when income drops and debts pile up, covering payment priority, creditor negotiation, collector defense using FDCPA rights, validation letters, statutes of limitations, settlement strategy, and consequences of nonpayment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill when income drops, bills are overdue, collectors are calling, or debt litigation risk needs practical triage. The skill helps an agent prioritize payments, draft collector and settlement letters, create reminders, and maintain debt-status records.

### Deployment Geography for Use:

Global; the skill contains US-specific legal references and directs agents to localize legal guidance for non-US users.

## Known Risks and Mitigations:

Risk: The skill can store sensitive debt, account, collector, lawsuit, and settlement details locally and across sessions.

Mitigation: Mask account numbers, ask before saving files or reminders, delete stored debt records when no longer needed, and consider installing a pinned version.

Risk: The skill contains US-specific legal references that may not apply to users in other jurisdictions.

Mitigation: Confirm the user's country and state or region before jurisdiction-specific guidance, substitute local legal equivalents, and cite current local sources.

## Reference(s):

- [Debt Survival ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/debt-survival)
- [Fair Debt Collection Practices Act, 15 U.S.C. 1692](https://www.law.cornell.edu/uscode/text/15/chapter-41/subchapter-V)
- [CFPB Debt Collection Rules, Regulation F](https://www.consumerfinance.gov/rules-policy/regulations/1006/)
- [Nolo Statute of Limitations on Debt Collection by State](https://www.nolo.com/legal-encyclopedia/statute-of-limitations-state-702.html)
- [CFPB Medical Debt and Credit Reports](https://www.consumerfinance.gov/about-us/newsroom/cfpb-kicks-off-rulemaking-to-remove-medical-bills-from-credit-reports/)
- [Federal Student Aid Default Guidance](https://studentaid.gov/manage-loans/default)
- [HUD Housing Counseling](https://www.hud.gov/counseling)
- [CFPB Complaint Portal](https://www.consumerfinance.gov/complaint/)
- [LawHelp Legal Aid Directory](https://www.lawhelp.org)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance, drafted letters, local text files, reminders, and structured debt-status records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use email, calendar, and filesystem tools; guidance should be localized and cited for the user's jurisdiction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
