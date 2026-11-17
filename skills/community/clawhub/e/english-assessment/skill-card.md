## Description:

An adaptive English assessment assistant that creates quizzes, scores responses, explains mistakes, and tracks learning progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-zihan](https://clawhub.ai/user/z-zihan)

### License/Terms of Use:

MIT-0

## Use Case:

English learners use this skill to assess university-level English (CEFR B1–C2), practice through adaptive quizzes, review mistakes, and track progress over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assessment scores and learning records are stored locally and may remain until deleted.

Mitigation: Review the stored records periodically and delete the skill's local data files when you want them removed.

Risk: Question searches send search keywords to external public sources, and the documented network allowlist is inconsistent.

Mitigation: Reconcile and enforce the allowed destinations if network restrictions matter; searches should contain only question-search keywords.

Risk: Optional Feishu backup uploads learning records to a cloud document whose sharing settings affect access.

Mitigation: Approve each backup only when comfortable with the upload and verify the destination document's sharing settings.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/z-zihan/skills/english-assessment)
- [Oxford Learner's Dictionaries](https://www.oxfordlearnersdictionaries.com/)
- [Vocabulary.com](https://www.vocabulary.com/)
- [Public CET-4/6 question collection](https://github.com/wamich/english-exem-md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Conversational text and Markdown for quizzes, scores, explanations, and progress reports; JSON for optional data export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive question-and-answer flow with adaptive difficulty; optional export and import of learning records.]

## Skill Version(s):

4.17.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
