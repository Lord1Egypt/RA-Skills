## Description:

A multi-agent double-blind A/B testing workflow for comparing AI models or agents across repeated rounds with coordinator, contestant, and judge roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluators use this skill to compare two AI models or agents with repeated blind judging, configurable rounds, and a structured final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Judge results can be misleading if the number of rounds, models, rubric, or output language are unclear.

Mitigation: Specify the round count, compared models or agents, scoring rubric, and preferred output language before running the workflow.

Risk: Contestant outputs may reveal model identity or other source clues, weakening the blind comparison.

Mitigation: Anonymize outputs before judging and remove identity markers such as model names or contestant labels.

Risk: Subagent timeouts or malformed judge responses can leave incomplete code, scores, or comments.

Mitigation: For code tasks, require complete code before runtime output; retry or re-run judging when required score tags are missing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prompts and structured JSON-style evaluation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may include contestant outputs, judge scores, comments, winners, aggregate totals, and confidence notes.]

## Skill Version(s):

1.1.0-en2 (source: release metadata; skill frontmatter is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
