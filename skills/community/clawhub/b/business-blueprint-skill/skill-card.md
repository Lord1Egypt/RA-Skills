## Description:

Generates business capability blueprints, domain-knowledge maps, and architecture diagrams from presales materials, meeting notes, or solution documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, solution architects, and presales teams use this skill to turn meeting notes, RFPs, and solution materials into canonical blueprint JSON, static viewers, and diagram exports for review or downstream report and slide workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from an untrusted source or moving target can expose users to unexpected code changes.

Mitigation: Install from a trusted release and verify the pinned release digest or commit before use.

Risk: Generated blueprint, viewer, projection, prompt-audit, and patch-log files may retain confidential meeting notes or RFP content.

Mitigation: Run the skill in a sandbox or virtual environment with only needed project files, and delete retained generated artifacts when they are no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaisersong/skills/business-blueprint-skill)
- [README](artifact/README.md)
- [GitHub v0.16.2 release](https://github.com/kaisersong/kai-business-blueprint/releases/tag/v0.16.2)
- [Blueprint schema reference](artifact/references/blueprint-schema.md)
- [Route eligibility reference](artifact/references/route-eligibility.md)
- [Evaluation README](artifact/evals/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON blueprints, shell commands, and generated diagram or viewer files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated local artifacts can include solution.blueprint.json, solution.projection.json, static HTML viewers, SVG, draw.io, Excalidraw, Mermaid exports, and JSON patch logs.]

## Skill Version(s):

0.16.2 (source: server release evidence and README current release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
