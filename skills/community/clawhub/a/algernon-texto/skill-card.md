## Description:

Algernon Texto guides OpenAlgernon study materials block by block with interactive reading, explanation, testing, mapping, and paper-reading modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antoniovfranco](https://clawhub.ai/user/antoniovfranco)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and study agents use this skill to read OpenAlgernon materials in manageable blocks, request explanations or examples, reflect between paper sections, and generate study cards from explored concepts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read material paths from the local OpenAlgernon database and material manifests.

Mitigation: Use it only with trusted OpenAlgernon databases and manifests, and validate slugs and resolved material paths before reading content.

Risk: Configured Notion credentials may cause generated concepts and flashcards to be uploaded.

Mitigation: Preview external exports and require explicit user confirmation before appending session content to Notion.

Risk: Session-derived summaries may be appended to local conversation memory.

Mitigation: Ask before saving local memory and avoid storing sensitive study material or personal notes unless the user confirms.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/antoniovfranco/skills/algernon-texto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and plain text with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally append generated study summaries and cards to configured Notion and local memory destinations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
