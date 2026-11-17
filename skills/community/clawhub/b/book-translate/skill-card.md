## Description:

Uses the platform text translation skill to automatically split and translate full books or long texts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackzhenguo](https://clawhub.ai/user/jackzhenguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate full books, research papers, technical documents, course materials, and long reports by splitting source content into chunks, translating each chunk, and merging the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential, regulated, or proprietary documents may be processed by the agent and translation model during full-text translation.

Mitigation: Use this skill only with content approved for that processing path, or avoid it for sensitive documents unless the deployment and model handling are acceptable.

Risk: Very long inputs can exceed token limits or fail partway through translation.

Mitigation: Use the skill's chunking approach, keep track of completed chunks, and resume from the last successful segment if translation is interrupted.

Risk: PDF translation depends on the quality of extracted source text.

Mitigation: Review or clean extracted PDF text before translation when document fidelity is important.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackzhenguo/skills/book-translate)
- [ClawHub publisher profile](https://clawhub.ai/user/jackzhenguo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text translated content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chunked translations are merged into a complete translated document while preserving paragraph structure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
