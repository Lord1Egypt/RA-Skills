## Description:

This skill helps agents manage RAGFlow datasets and documents, start or stop parsing, check parse status, run retrieval searches, and list configured models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redredrrred](https://clawhub.ai/user/redredrrred)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage RAGFlow datasets, documents, parsing workflows, retrieval queries, and model listings from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and uploaded documents may be sent to an untrusted or non-HTTPS RAGFlow endpoint.

Mitigation: Use HTTPS or a loopback development URL, trust the configured endpoint, and use a narrowly scoped RAGFlow API key.

Risk: Uploaded files may contain sensitive content that is transmitted to the configured RAGFlow service.

Mitigation: Avoid uploading sensitive files unless the endpoint and network path are trusted.

Risk: Dataset and document delete actions can remove content when explicit IDs are supplied.

Mitigation: List the exact datasets or documents first and require explicit user confirmation before deletion.

## Reference(s):

- [Output Format Reference](artifact/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/redredrrred/skills/2026-3-22dataset)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, tables, and JSON blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May relay exact RAGFlow API fields, messages, and errors returned by the bundled scripts.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
