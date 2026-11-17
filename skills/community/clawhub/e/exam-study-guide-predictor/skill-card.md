## Description:

Creates a source-bound study guide and evidence-ranked exam prediction from a student's own course materials, including biology-family courses and English or Arabic professor transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samdozer](https://clawhub.ai/user/samdozer)

### License/Terms of Use:

MIT-0

## Use Case:

External students use this skill to turn their own authorized course materials into an exam-focused study guide, predicted questions, model answers, and optional flashcards. It is intended for preparation before an exam, not writing an exam or cheating during a live assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide materials they are not allowed to use or may attempt to use the skill during a live exam.

Mitigation: Use the skill only before an exam and only with course materials the user is authorized to study from.

Risk: Predicted exam questions can be mistaken for guaranteed exam content.

Mitigation: Keep predictions confidence-ranked and evidence-justified, and separate explicit professor statements from inferred predictions.

Risk: Generated study outputs depend on the completeness and accuracy of user-provided sources.

Mitigation: Ask for past papers, official model answers, mark distribution, and professor transcripts before producing final guidance.

## Reference(s):

- [Output Format & Section Catalog](references/output-format.md)
- [Prediction & Analysis Method](references/prediction-and-analysis.md)
- [Server-resolved GitHub provenance](https://github.com/SamDozer/exam-study-guide-predictor/tree/main/exam-study-guide-predictor)
- [ClawHub skill page](https://clawhub.ai/samdozer/skills/exam-study-guide-predictor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [HTML or Word .docx study guide, with optional Anki-ready CSV flashcards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs default to English, may parse Arabic or code-switched transcripts, and should keep explicit professor statements separate from inferred predictions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
