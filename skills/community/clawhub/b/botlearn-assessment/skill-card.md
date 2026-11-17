## Description:

botlearn-assessment is a BotLearn five-dimension capability self-assessment skill for reasoning, retrieval, creation, execution, and orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run autonomous agent capability assessments, review per-dimension scores, and track results over time through generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform autonomous assessment steps, including searches or local report generation, after broad assessment-related triggers.

Mitigation: Install only when that behavior is intended, and narrow triggers or add confirmation steps before use in shared agent environments.

Risk: The skill saves detailed Markdown, HTML, JSON, and SVG assessment results that may include sensitive prompt, answer, or scoring content.

Mitigation: Review result files before sharing, clean up saved reports when no longer needed, and avoid running assessments with confidential material unless storage is acceptable.

Risk: Generated HTML and SVG reports may carry report-rendering safety concerns.

Mitigation: Review or patch the bundled report generators before opening reports in sensitive contexts or distributing generated HTML/SVG files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-assessment)
- [README](README.md)
- [Skill entry point](SKILL.md)
- [Full exam flow](flows/full-exam.md)
- [Dimension exam flow](flows/dimension-exam.md)
- [Exam execution flow](flows/exam-execution.md)
- [Report generation flow](flows/generate-report.md)
- [Scoring strategy](strategies/scoring.md)
- [Exam report schema](assets/exam-report-schema.json)
- [D1 Reasoning questions](questions/d1-reasoning.md)
- [D2 Retrieval questions](questions/d2-retrieval.md)
- [D3 Creation questions](questions/d3-creation.md)
- [D4 Execution questions](questions/d4-execution.md)
- [D5 Orchestration questions](questions/d5-orchestration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, HTML, JSON, SVG, and inline text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates assessment result files under results/ and may invoke bundled Node.js report generators when available.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter and README list 0.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
