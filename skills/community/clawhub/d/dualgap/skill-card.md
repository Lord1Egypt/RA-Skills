## Description:

DualGap turns two research-paper PDF collections, arXiv downloads, or research directions into reviewer-checked literature notes, direction-level syntheses, cross-domain comparison, research-gap analysis, and ranked improvement ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zza234s](https://clawhub.ai/user/zza234s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research-planning teams use this skill to compare two research directions from PDF folders and produce evidence-grounded literature notes, syntheses, research gaps, and ranked follow-up ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends extracted PDF content and API credentials to a configurable OpenAI-compatible endpoint.

Mitigation: Use only a trusted HTTPS endpoint, confirm the PDFs may be shared with that provider, and use a restricted API key stored outside generated outputs.

Risk: Generated output directories may contain extracted paper text, raw model responses, notes, reviews, and audit artifacts.

Mitigation: Keep output directories private and review artifacts before sharing or committing them.

Risk: The self-validation path can invoke a sibling skill-creator validator when present.

Mitigation: Run self-validation in a workspace where sibling tooling is trusted, or inspect the sibling validator before executing it.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zza234s/DualGap)
- [ClawHub skill page](https://clawhub.ai/zza234s/skills/dualgap)
- [Note schema](references/note_schema.md)
- [Validation protocol](references/validation_protocol.md)
- [Configuration example](references/config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, JSONL, plain text, and command-line instructions written to an output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces extracted texts, per-paper notes, review records, synthesis documents, ranked improvement ideas, workflow manifests, and audit reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
