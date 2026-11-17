## Description:

Helps developers assess code review feedback against their codebase, respond with evidence, and implement verified suggestions when authorized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage PR or MR feedback, explain disagreements with evidence, and apply and verify approved fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying incorrect review suggestions could introduce regressions.

Mitigation: Verify each finding against the codebase, test individual fixes, and re-review patches before marking them resolved.

Risk: The agent could edit code or publish PR replies without the required authority.

Mitigation: Limit changes to authorized scope, obtain explicit approval for external replies, and escalate uncertain decisions in headless mode.

## Reference(s):

- [ClawHub release](https://clawhub.ai/iliaal/skills/compound-eng-receiving-code-review)
- [Feedback triage](references/feedback-triage.md)
- [Evidence and disagreement](references/evidence-and-disagreement.md)
- [Fix and handoff](references/fix-and-handoff.md)
- [Headless mode](references/headless-mode.md)
- [Review modes](references/review-modes.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands]

**Output Format:** [Markdown findings and dispositions, with optional code changes or command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Headless use returns structured triage results; review-only use stops at findings and recommendations.]

## Skill Version(s):

5.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
