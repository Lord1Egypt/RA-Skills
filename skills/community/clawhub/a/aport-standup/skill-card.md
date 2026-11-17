## Description:

Generate a standup update from APort policy decisions, showing what was shipped from signed decision records rather than memory or estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uchibeke](https://clawhub.ai/user/uchibeke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and teams use this skill to turn recent APort policy decisions into factual daily standups, weekly summaries, team status updates, blocker lists, and audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path includes mutable remote instructions from the APort site.

Mitigation: Review the setup path before installation and do not treat remote APort site instructions as authoritative skill behavior.

Risk: The setup guidance includes unpinned local package execution through npx.

Mitigation: Avoid running unpinned npx commands unless the package source is trusted.

Risk: Generated standups can expose work history, policy outcomes, blockers, and decision identifiers.

Mitigation: Treat generated standups as sensitive and share them only with appropriate recipients.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/uchibeke/skills/aport-standup)
- [Publisher Profile](https://clawhub.ai/user/uchibeke)
- [APort Passport](https://aport.id)
- [APort Agent Skill](https://aport.id/skill)
- [APort Decisions API](https://aport.io/api/verify/decisions/YOUR_AGENT_ID)
- [APort Decision Verification API](https://aport.io/api/verify/decisions/get/DECISION_ID)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown standup summaries with inline API request examples and decision IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an APort passport and APORT_AGENT_ID; outputs may include sensitive work history and policy-decision details.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
