## Description:

Helps agents evaluate code review feedback against the codebase, respond with evidence, and implement verified suggestions within authorized scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess PR/MR review comments, classify findings, prepare evidence-based replies, and make verified fixes within authorized scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan notes a possible mismatch between the code-review purpose and evaluation tooling; the scan could not assess script internals.

Mitigation: Before installing, check whether the evaluation and diagnostic tooling fits your intended use, and review scripts before running them.

## Reference(s):

- [Evidence and disagreement](artifact/references/evidence-and-disagreement.md)
- [Feedback triage](artifact/references/feedback-triage.md)
- [Fix and handoff](artifact/references/fix-and-handoff.md)
- [Headless mode](artifact/references/headless-mode.md)
- [Review modes](artifact/references/review-modes.md)
- [ClawHub skill release](https://clawhub.ai/iliaal/skills/compound-eng-receiving-code-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code]

**Output Format:** [Evidence-based review triage and responses in Markdown, with scoped code changes when authorized.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Classifies findings and reports supporting evidence and remaining uncertainty.]

## Skill Version(s):

5.1.7 (source: server-resolved release metadata, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
