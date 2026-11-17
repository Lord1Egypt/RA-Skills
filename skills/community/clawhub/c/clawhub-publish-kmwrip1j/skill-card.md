## Description:

Analyze a user's MBTI from authorized OpenClaw memory, session history, and workspace notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofsoysauce](https://clawhub.ai/user/kingofsoysauce)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in OpenClaw to infer a best-fit MBTI hypothesis from authorized conversation history, workspace memory, and related notes. It produces evidence-backed reports, confidence notes, adjacent-type comparisons, and follow-up questions when uncertainty remains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect broad OpenClaw and workspace history, including memory, sessions, task metadata, and cron metadata.

Mitigation: Authorize only the narrowest source categories needed and avoid task or cron sources unless they are necessary for the analysis.

Risk: Generated outputs may persist private excerpts and derived personality evidence in the report directory.

Mitigation: Use a private output directory, limit quoting when possible, review generated files, and delete ./.mbti-reports after use.

Risk: The optional --open flag launches the generated local HTML report in the default browser.

Mitigation: Omit --open on shared or restricted machines and open the report manually only after reviewing the output path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofsoysauce/skills/clawhub-publish-kmwrip1j)
- [OpenClaw](https://openclaw.ai/)
- [Interactive report demo](https://kingofsoysauce.github.io/mbti-skill/)
- [Analysis Framework](references/analysis_framework.md)
- [Evidence Rubric](references/evidence_rubric.md)
- [Report Copy Contract](references/report_copy_contract.md)
- [Report Structure](references/report_structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; generated reports in HTML, Markdown, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports to ./.mbti-reports/<timestamp>/ by default; may open local HTML when --open is used.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
