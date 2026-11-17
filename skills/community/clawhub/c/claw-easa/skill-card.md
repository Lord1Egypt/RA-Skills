## Description:

Query EASA Easy Access Rules locally with exact reference lookup, full-text search, and semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dmoraine](https://clawhub.ai/user/dmoraine)

### License/Terms of Use:

MIT-0

## Use Case:

Aviation regulatory users, developers, and agents use this skill to retrieve EASA rule text, AMC/GM guidance, and FAQ material from a local claw-easa corpus before drafting answers to regulatory questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions run bootstrap scripts from a mutable GitHub checkout.

Mitigation: Review the repository and pin a trusted commit before running bootstrap, install, or runtime-check scripts.

Risk: Install and ingestion commands can create or update the local EASA corpus, and faq-all crawls many EASA FAQ pages.

Mitigation: Run ingestion only when corpus updates are intended; prefer targeted FAQ ingestion where possible and keep the default crawl delay unless there is a reviewed reason to change it.

Risk: Answers can be incomplete or misleading if the local corpus or index is unavailable, stale, or scoped incorrectly.

Mitigation: Run claw-easa status before use, use exact lookup for references, scope broad searches with --slug when appropriate, and state clearly when retrieval is empty or ambiguous.

## Reference(s):

- [claw-easa Skill Usage](references/usage.md)
- [claw-easa Runtime Setup](references/runtime-setup.md)
- [EASA Answering Notes](references/easa-answering.md)
- [EASA FAQ Regulations](https://www.easa.europa.eu/en/the-agency/faqs/regulations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown answers with cited excerpts and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local claw-easa CLI and an available local EASA corpus or index.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
