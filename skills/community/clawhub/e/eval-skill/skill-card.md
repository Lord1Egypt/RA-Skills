## Description:

Evaluates an agent skill by having three independent child evaluators score it across eight documented quality dimensions and then summarizing the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[54lynnn](https://clawhub.ai/user/54lynnn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill reviewers use this skill to perform structured reviews of ClawHub agent skills, including scores for functionality, code quality, robustness, security, documentation, dependencies, expected runtime behavior, and overall quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the selected skill directory and forwards full text contents to child evaluators.

Mitigation: Avoid running it on directories that contain secrets, private configuration, credentials, or unrelated sensitive files.

Risk: Adversarial skill text may influence child evaluators during review.

Mitigation: Treat findings about adversarial or untrusted skills cautiously and review the final report before acting on it.

## Reference(s):

- [Evaluation Protocol](references/evaluation-protocol.md)
- [ClawHub Skill Page](https://clawhub.ai/54lynnn/skills/eval-skill)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown report with score tables, disagreement analysis, consensus strengths and issues, and a final recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report expects each child evaluator to provide a JSON score summary delimited by SCORE_SUMMARY markers.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter says 1.5.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
