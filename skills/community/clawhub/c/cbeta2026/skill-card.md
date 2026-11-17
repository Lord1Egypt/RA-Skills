## Description:

大藏经CBETA2026 supports Simplified Chinese CBETA scripture lookup and Buddhist citation verification with simple Q&A and deeper research modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gouchunlei2-png](https://clawhub.ai/user/gouchunlei2-png)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to retrieve Buddhist canon passages, verify citations, compare related texts, and produce CBETA-formatted source tables with scripture locations and online links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used for citation-sensitive religious or academic work where unsupported text could mislead readers.

Mitigation: Require CBETA source locations for claims and explicitly state when the subscribed corpus does not cover the requested material.

Risk: Document editing through Tencent Docs or local docx tooling could alter user materials.

Mitigation: Confirm user intent before allowing document edits and keep citation-checking separate from destructive document changes.

Risk: The corpus is disclosed as Simplified Chinese CBETA content, which may limit coverage for some lookup tasks.

Mitigation: Treat corpus coverage as a known limitation and avoid filling gaps from unsourced assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gouchunlei2-png/skills/cbeta2026)
- [CBETA Online](https://cbetaonline.dila.edu.tw/zh/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown answers, research summaries, citation tables, and CBETA online links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to cite CBETA source locations and state coverage limitations when the subscribed corpus does not contain enough evidence.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
