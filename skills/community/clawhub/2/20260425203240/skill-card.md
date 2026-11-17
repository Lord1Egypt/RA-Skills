## Description:

OUA v2.0 is an engineering-focused AI assessment framework that combines OIT intelligence-ceiling checks with LLI engineering-readiness checks across 13 dimensions and 104 test questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafeyu8899](https://clawhub.ai/user/rafeyu8899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluators use this skill to administer structured AI capability assessments, score model performance, and produce reports that compare intelligence, engineering reliability, tool-use accuracy, delivery satisfaction, and self-improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may run unsafe browser code from unescaped input and an unpinned CDN dependency.

Mitigation: Review result files before report generation, escape report metadata before sharing, and bundle or pin Chart.js with integrity before operational use.

Risk: Generated reports may contain raw prompts, model outputs, and evaluator notes.

Mitigation: Review reports for sensitive or unintended content before distributing them.

## Reference(s):

- [Skill Definition](artifact/SKILL.md)
- [OUA v2.0 Test Bank](artifact/references/test-bank-v2.md)
- [OUA v1.0 Test Bank](artifact/references/test-bank.md)
- [OUA v2.0 Weight Revision](artifact/OUA-v2.0-weight-revision.md)
- [OUA v2.0 Upgrade Plan](artifact/OUA-v2.0-upgrade-plan.md)
- [Scoring Script](artifact/scripts/score_test.py)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with structured assessment instructions and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide scoring workflows that produce an HTML report from provided result data.]

## Skill Version(s):

2.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
