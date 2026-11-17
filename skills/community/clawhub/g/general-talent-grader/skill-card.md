## Description:

General Talent Grader evaluates resumes, interview records, and job descriptions to assign L1-L4 talent levels, audit resume credibility, generate follow-up interview questions, and produce role-adaptive competency scorecards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Hiring teams and recruiters use this skill to audit resumes, cross-check interview evidence, and produce role-adaptive L1-L4 candidate assessments for product, engineering, operations, sales, management, design, data, HR, finance, and marketing roles. It is not intended for employee performance reviews, promotion reviews, training-needs analysis, or regulated credentialing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive candidate and hiring material.

Mitigation: Get explicit user intent before analysis, redact unnecessary personal identifiers, avoid retaining candidate files, and limit outputs to the hiring review task.

Risk: Generated scores can influence hiring decisions even when evidence is incomplete.

Mitigation: Treat scores as heuristic review aids, require quoted source evidence for each scored signal, mark low-confidence dimensions, and keep a human reviewer accountable for decisions.

Risk: Scoring and tooling inconsistencies could produce incorrect levels.

Mitigation: Verify or replace the mismatched score validator before relying on numeric levels, and run consistency checks for high or low scores, non-balanced profiles, and L4 claims.

## Reference(s):

- [General Talent Grader on ClawHub](https://clawhub.ai/tuobadaidai/skills/general-talent-grader)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Resume Audit Guide](artifact/references/resume_audit.md)
- [Quantitative Thresholds](artifact/references/quantitative_thresholds.md)
- [Behavioral Anchors](artifact/references/behavioral_anchors.md)
- [Signal Extraction](artifact/references/signal_extraction.md)
- [Cognitive Depth Checks](artifact/references/cognitive_depth.md)
- [Pre-flight Check](artifact/references/pre-flight-check.md)
- [Known Issues](artifact/references/known-issues.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with score tables, audit findings, follow-up interview questions, and optional shell commands for score validation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite candidate-provided evidence, mark uncertain dimensions, and treat scores as heuristic review aids.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
