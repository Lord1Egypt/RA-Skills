## Description: <br>
Analyze a user's MBTI from authorized OpenClaw memory, session history, and workspace notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofsoysauce](https://clawhub.ai/user/kingofsoysauce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and agent operators use this skill to generate an evidence-backed MBTI hypothesis from approved local memory, session history, and workspace notes. It supports personality inference without a questionnaire while preserving uncertainty, adjacent-type comparisons, and source traceability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is privacy-sensitive because it analyzes local history, memory, session records, and optional task or cron metadata for personality inference. <br>
Mitigation: Approve only the source categories needed for the run, avoid task or cron metadata unless intentionally included, and delete the .mbti-reports output when it is no longer needed. <br>
Risk: Generated reports may contain short excerpts from approved local sources. <br>
Mitigation: Use quote-mode none when excerpts should be excluded, and review report.html, report.md, and evidence_pool.json before sharing. <br>
Risk: MBTI output can be mistaken for a definitive psychological assessment. <br>
Mitigation: Treat the result as a best-fit, non-clinical hypothesis and keep confidence, counterevidence, adjacent-type comparisons, and follow-up uncertainty visible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofsoysauce/clawhub-publish-kmwrip1j) <br>
- [OpenClaw](https://openclaw.ai/) <br>
- [Interactive report demo](https://kingofsoysauce.github.io/mbti-skill/) <br>
- [Analysis Framework](references/analysis_framework.md) <br>
- [Evidence Rubric](references/evidence_rubric.md) <br>
- [Report Copy Contract](references/report_copy_contract.md) <br>
- [Report Structure](references/report_structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [HTML, Markdown, and JSON files with concise chat guidance and shell command steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary outputs include report.html, report.md, analysis_result.json, and evidence_pool.json in a local .mbti-reports directory.] <br>

## Skill Version(s): <br>
0.4.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
