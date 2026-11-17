## Description:

Summarizes technical documents into structured Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelevis](https://clawhub.ai/user/kelevis)

### License/Terms of Use:


## Use Case:

Developers and reviewers use this skill to summarize technical documents, extract key points, and surface potential risks in a concise Markdown structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may cause the skill to be selected for generic text-analysis requests.

Mitigation: Provide sensitive content only when summarization is intended for the current session.

Risk: Generated summaries and risk lists may omit nuance from the source document.

Mitigation: Review the Markdown output against the original document before relying on it for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelevis/skills/demo)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown with summary, key points, and risks sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns valid Markdown only; the summary is capped at five lines by the skill behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
