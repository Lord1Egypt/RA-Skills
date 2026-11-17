## Description:

bagua-furnace turns dense knowledge materials such as books, courses, notes, transcripts, discussions, webpages, PDFs, and media-derived text into reusable, source-anchored methodology cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract transferable methods, decision frameworks, and thinking models from supplied knowledge materials. The output is intended for local methodology libraries and downstream reasoning skills rather than executable agent-skill generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags default local logging and persistent anonymous identifiers.

Mitigation: Tell users that local method-layer logging is enabled by default, document the opt-out controls, and avoid processing confidential material unless temporary files and local logs are isolated.

Risk: The security evidence flags cloud-related hooks and external endpoints.

Mitigation: Keep cloud sync disabled unless the user explicitly enables it, and disclose when remote endpoints are used for signal sync, registration, proposals, or media transcription.

Risk: The security evidence flags creator-token and proposal workflows that can lead to persistent local changes.

Mitigation: Require manual review of proposal contents and diffs before applying local edits, and avoid approving proposals while sensitive credentials or private source material are in scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j-levee/skills/bagua-furnace)
- [Introduction](references/intro.md)
- [Ingestion workflow](references/ingestion.md)
- [Extraction lenses](references/extraction-lenses.md)
- [Method card schema](references/method-card-schema.md)
- [Long-text distillation SOP](references/long-text-distillation.md)
- [Security audit](references/security-audit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown methodology cards, concise guidance, and command/configuration snippets when required by an ingestion or indexing workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Method cards are expected to preserve source anchors, confidence labels, routing metadata, and boundary conditions.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter reports 1.2.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
