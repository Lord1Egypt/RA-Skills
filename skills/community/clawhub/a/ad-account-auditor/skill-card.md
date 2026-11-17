## Description:

Audits a paid ad account for incremental contribution, wasted spend, and measurement integrity before scaling by running a typed 20-item ROAS profile with verified vetoes and a SHIP/FIX/BLOCK/UNDECIDED gate on user-provided exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators, analysts, and agents use this skill to audit one paid-media account or portfolio before launch or scale. It reviews normalized spend, outcome, attribution, economics, placement, and claims evidence to produce an audit verdict, unknowns, and prioritized fixes without changing campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive ad-account exports, order or lead IDs, attribution data, and business constraints.

Mitigation: Use only authorized exports, avoid unnecessary persistence, and write audit artifacts only when explicitly authorized.

Risk: Audit output could be mistaken for permission to mutate campaigns, bids, audiences, or budgets.

Mitigation: Treat the skill as audit and reporting only; require separate explicit approval before any ad-account change.

Risk: Missing own-data truth, placement evidence, attribution windows, currency, conversion lag, or business constraints can make scores unreliable or undecidable.

Mitigation: Collect the required context and mark missing qualified items as unknown instead of renormalizing or treating absent data as a pass.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/ad-account-auditor)
- [Publisher Profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Standalone Auditor Runtime](references/auditor-runtime.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown audit report with explicit status, verdict, score state, evidence unknowns, reconciliation details, and prioritized fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not modify ad accounts; persistent audit artifacts are written only after explicit authorization.]

## Skill Version(s):

19.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
