## Description:

Generate professional presentations with Gamma AI from a topic, outline, or full content brief, with PDF or PPTX output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmanchu](https://clawhub.ai/user/lmanchu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to create presentation decks from a topic or prepared content without manually designing slides. It is suited for pitch decks, talks, roadmaps, and other presentation workflows where Gamma generates the slide design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation topics and source content are sent to Gamma for generation.

Mitigation: Use only content approved for Gamma processing; avoid confidential, regulated, or sensitive material unless organizational policy allows it.

Risk: The skill requires access to a Gamma API key.

Mitigation: Use a dedicated, scoped key stored in a secure environment variable or managed configuration, and avoid broad shared keys where possible.

Risk: Generated presentations are downloaded from an API-provided Gamma URL.

Mitigation: Review export URL handling and downloaded files before broader deployment, especially in automated or shared environments.

Risk: The README includes an unpinned npx install path.

Mitigation: Pin install sources or verify package provenance before use in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lmanchu/skills/gamma-presentation)
- [Publisher profile](https://clawhub.ai/user/lmanchu)
- [Gamma](https://gamma.app)
- [Gamma public API endpoint](https://public-api.gamma.app/v1.0)
- [Bun runtime](https://bun.sh)

## Skill Output:

**Output Type(s):** [files, text, shell commands, configuration, guidance]

**Output Format:** [PDF or PPTX deck files, Gamma URLs, JSON status output, and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bun and a Gamma API key; accepts topic or content, optional slide count, output format, and output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
