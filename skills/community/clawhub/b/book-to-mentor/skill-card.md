## Description:

Converts a user-provided book or document into a reusable mentor skill with source-grounded explanations, guided practice, and learning records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gengwenhao](https://clawhub.ai/user/gengwenhao)

### License/Terms of Use:

MIT

## Use Case:

Learners use the skill to turn their own books or documents into source-linked study mentors for explanations, practice, quick reference, and ongoing learning records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reading a broad private directory could expose more document content to the agent than intended.

Mitigation: Provide only the specific book or document paths you want extracted.

Risk: Generated mentor files and learning records are stored locally.

Mitigation: Choose an appropriate output directory and review saved learning records for sensitive information.

Risk: An optional update check contacts GitHub.

Mitigation: Run the update check only when you intend to make that network request.

## Reference(s):

- [Supported formats and extraction limits](artifact/docs/formats.md)
- [Learning record contract](artifact/docs/state-schema.en.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, JSON, Guidance]

**Output Format:** [Local mentor files, source-linked study guidance, and JSON learning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discloses incomplete extraction and retains learning records across mentor updates.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata and bundled release.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
