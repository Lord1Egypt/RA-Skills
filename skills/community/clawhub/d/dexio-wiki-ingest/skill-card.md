## Description:

Guides agents to ingest sources into a wiki with immutable raw copies, claim-level citations, and updates to relevant pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexio](https://clawhub.ai/user/dexio)

### License/Terms of Use:

MIT-0

## Use Case:

Wiki maintainers and agents use this skill to add articles, papers, notes, or datasets to an LLM wiki while updating related pages and preserving source attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copying sensitive or restricted source material into persistent wiki files.

Mitigation: Ingest only content permitted to be stored; exclude secrets and private data, and summarize or link to restricted sources instead.

## Reference(s):

- [Wiki Ingest (Dexio) on ClawHub](https://clawhub.ai/dexio/skills/dexio-wiki-ingest)
- [dexio publisher profile](https://clawhub.ai/user/dexio)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown wiki-page updates and raw source files with YAML frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source hashes, claim-level citations, trust labels, and per-page change notes.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
