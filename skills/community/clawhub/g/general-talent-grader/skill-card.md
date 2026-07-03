## Description: <br>
General Talent Grader helps agents audit resumes, interview notes, and job descriptions to produce role-adaptive L1-L4 candidate assessments, follow-up interview questions, cognitive review notes, and score-consistency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring managers, and interview reviewers can use this skill as decision support for resume audits, interview retrospectives, candidate level calibration, and role-fit analysis. It is not a substitute for human hiring judgment or applicable employment, privacy, and anti-discrimination review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process sensitive candidate materials such as resumes and interview notes. <br>
Mitigation: Use it only with candidate materials the reviewer is allowed to process, redact unnecessary personal data, and confirm before analyzing uploaded files. <br>
Risk: The skill can produce employment-impacting L1-L4 grades. <br>
Mitigation: Treat grades as decision support and require human hiring review before any employment decision. <br>
Risk: Legacy ai-talent-grader references may affect scoring consistency. <br>
Mitigation: Use the included consistency checks, known-issues notes, and score validator to review high-impact or borderline assessments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuobadaidai/general-talent-grader) <br>
- [README](README.md) <br>
- [Resume audit guide](references/resume_audit.md) <br>
- [Quantitative thresholds](references/quantitative_thresholds.md) <br>
- [Behavioral anchors](references/behavioral_anchors.md) <br>
- [Signal extraction guide](references/signal_extraction.md) <br>
- [Cognitive depth checks](references/cognitive_depth.md) <br>
- [Pre-flight checklist](references/pre-flight-check.md) <br>
- [Known issues](references/known-issues.md) <br>
- [Score validator](scripts/validate_scores.py) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown reports with structured scorecards, quoted evidence, follow-up interview questions, and optional shell commands for score validation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include L1-L4 levels, six-dimension scores, confidence notes, inconsistency flags, risk signals, and suggested follow-up questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
