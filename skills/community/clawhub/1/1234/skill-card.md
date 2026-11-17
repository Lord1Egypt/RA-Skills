## Description:

Use for RAGFlow dataset and retrieval tasks: create, list, inspect, update, or delete datasets; list, upload, update, or delete documents in a dataset; start or stop parsing uploaded documents; check parser status through `parse_status.py`; and retrieve relevant chunks from RAGFlow datasets with `search.py`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caesergattuso](https://clawhub.ai/user/caesergattuso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage RAGFlow datasets, upload and parse documents, inspect parsing status, retrieve relevant chunks, and list configured models through bundled scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist a live RAGFlow API key in plaintext when credential memory is used.

Mitigation: Use a minimally scoped bearer token, avoid saving credentials unless the memory file is protected, and prefer secure prompting or an API key file.

Risk: Dataset and document operations can modify or delete RAGFlow content.

Mitigation: Manually verify exact dataset and document IDs before delete or stop operations, and require explicit confirmation before destructive actions.

Risk: Documents and metadata are sent to the configured RAGFlow server.

Mitigation: Use only trusted RAGFlow servers and HTTPS for non-local deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caesergattuso/skills/1234)
- [Publisher Profile](https://clawhub.ai/user/caesergattuso)
- [Output Format Reference](artifact/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON script output for exact downstream reporting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
