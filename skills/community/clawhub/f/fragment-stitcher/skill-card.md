## Description:

碎片知识缝纫师 helps users collect scattered notes and files, identify relationships among knowledge fragments, and generate connection notes or outline drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teamoplum](https://clawhub.ai/user/teamoplum)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers, researchers, product teams, and developers use this skill to organize fragmented notes from text, documents, meetings, and web sources into a local knowledge base. It helps them find related fragments and draft Markdown connection notes, PRD supplements, weekly summaries, and topic outlines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ingest user-provided local files and persist their contents in a configured knowledge base.

Mitigation: Confirm the file path and sensitivity of the content before collection, and avoid storing secrets, private chats, or sensitive business files unless local persistence is acceptable.

Risk: Generated fragments, connection notes, and outlines may retain sensitive source material in local knowledge files.

Mitigation: Review and delete generated knowledge files when they are no longer needed or when they include sensitive content.

Risk: Relationship notes and outline drafts are heuristic and may overstate or miss connections between fragments.

Mitigation: Review generated connections and outlines before relying on them for decisions or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teamoplum/skills/fragment-stitcher)
- [Fragment metadata fields](artifact/references/fields.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, JSON-like Python dictionaries, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist user-provided fragments, connection notes, and outlines to a configured local knowledge base.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
