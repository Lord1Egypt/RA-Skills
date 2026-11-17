## Description:

Context Manager helps agents collect, tag, connect, and review personal context so users can build thought trees, cognitive maps, decision recall, and AI-assistance boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize personal context from notes, chats, documents, internal reflections, and decisions into tagged records, thought trees, cognitive maps, and review outputs. It is best suited for workflows where human judgment remains the final decision point.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive personal context locally.

Mitigation: Use a dedicated local context directory, avoid importing secrets or third-party private chats/documents without permission, and apply appropriate privacy and retention controls.

Risk: File-path handling may write outside intended folders.

Mitigation: Review generated paths before use and add path validation before running the skill on shared or sensitive systems.

Risk: Bundled tagging and knowledge-workflow helpers may process untrusted IDs or indexes.

Mitigation: Do not run these helpers on untrusted inputs until IDs, indexes, and source paths are validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lj22503/skills/context-manager-v1)
- [Subfunction details](artifact/references/子功能详解.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, JSON-like records, and Python/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local context records, logs, trees, and review files under the configured context directory.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
