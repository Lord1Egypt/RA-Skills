## Description:

Compresses long text into structured 4D vectors to reduce token use while preserving core meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to condense long Chinese-oriented text into structured summaries or 4D vector-style representations. It is suited for text review, knowledge notes, dialogue compression, and token budget reduction after users provide plain text input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers such as "compress" and "压缩" may invoke the skill more often than expected.

Mitigation: Install it only when this text-compression behavior is desired, and adjust triggers or priority if the agent platform supports that.

Risk: Compression can omit nuance or expand already concise dialogue and emotional text.

Mitigation: Review compressed output before using it as an authoritative record or decision input.

Risk: The skill does not directly process EPUB or PDF books.

Mitigation: Convert documents to plain text before asking the skill to compress them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/largetool/skills/4d-compression-core)
- [Version Selection Protocol](artifact/VERSION_PROTOCOL.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown or JSON structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rule-based routing selects compression version A, B, or C based on text type; no executable payload or network behavior is indicated by the security evidence.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
