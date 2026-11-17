## Description:

Generates three differentiated sets of Chinese exam practice questions from a knowledge_map.json file, writes structured questions, renders a tabbed HTML exam page, and guides the learner to the next study step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoucha833-lang](https://clawhub.ai/user/zhoucha833-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Learners, tutors, and education-focused agents use this skill to turn an existing exam knowledge map into staged practice exams covering basic review, applied understanding, and final simulation. It is intended for workspace use where generated question JSON and HTML files can be reviewed before sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include unescaped content from notes, knowledge-map values, or generated question text.

Mitigation: Use the skill only with trusted or reviewed study materials until inserted HTML content is escaped or sanitized.

Risk: The rendered exam page loads third-party KaTeX scripts from a CDN.

Mitigation: Bundle trusted local assets or use integrity-protected CDN resources before sharing generated HTML in sensitive environments.

Risk: Reruns may overwrite prior generated exam outputs.

Mitigation: Use explicit invocation phrases and confirm the desired output before rerunning the question generation workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhoucha833-lang/skills/exam-question-generator)
- [Difficulty Rules](artifact/references/difficulty-rules.md)
- [Question Format Rules](artifact/references/question-formats.md)

## Skill Output:

**Output Type(s):** [text, JSON, HTML, guidance]

**Output Format:** [Structured questions.json plus a rendered HTML exam page and a concise follow-up message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates three 100-point practice exam sets with answers, explanations, scoring metadata, and tabs for basic, intermediate, and advanced practice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
