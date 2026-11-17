## Description:

Transform lengthy academic papers into concise, structured 250-word abstracts capturing background, methods, results, and conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and research teams use this skill to condense academic papers, theses, and technical reports into structured abstracts for literature review, submission drafting, and rapid paper triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL input path can fetch arbitrary addresses supplied by the user.

Mitigation: Avoid private, signed, internal, localhost, and cloud-metadata URLs; prefer local PDF or text input until URL fetching is restricted and dependencies are pinned.

Risk: Draft abstracts may misstate statistics, omit nuance, or overstate conclusions.

Mitigation: Review every generated abstract against the source paper and verify numbers, significance claims, and conclusions before submission or publication.

Risk: The skill works from text extraction and cannot interpret figures, charts, or image-only content.

Mitigation: Manually review visual, tabular, and scanned content and confirm that the input text is complete before relying on the abstract.

## Reference(s):

- [Abstract Templates by Discipline](references/abstract-templates.md)
- [Evaluation Rubric for Abstract Quality](references/evaluation-rubric.md)
- [Computer Science and Biomedical Example Abstracts](references/example-abstracts/cs-and-biomed-examples.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/abstract-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown or plain text abstract with background, objective, methods, results, conclusion, and word count.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for concise 250-word abstracts and optional file output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
