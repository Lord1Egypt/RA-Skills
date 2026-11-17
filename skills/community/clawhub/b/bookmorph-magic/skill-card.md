## Description:

Orchestrates book-to-content workflows that package a selected book into video, audio, cover images, and a manifest for an episode or campaign.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oiioai](https://clawhub.ai/user/oiioai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to connect book-selection, longform generation, and cover-generation adapters, then bundle the outputs into a stable episode package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can delete or write outside the intended output folder when configured unsafely.

Mitigation: Use a trusted, dedicated output root, independently check target paths, avoid custom episode directory prefixes, and use --clear-existing only after confirming the destination.

Risk: The skill relies on external adapters for book selection, longform media, and cover generation.

Mitigation: Review adapter outputs before bundling and record failed or partial runs in manifest.json for audit and retry workflows.

## Reference(s):

- [BookMorph Magic ClawHub skill page](https://clawhub.ai/oiioai/skills/bookmorph-magic)
- [Adapter contracts](references/integration-template.md)
- [Manifest fields](references/manifest-schema.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON manifest outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an episode directory containing video, audio, three cover images, and manifest.json when adapters supply source artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
