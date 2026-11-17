## Description:

Generate serialized comic-drama episodes through a fixed multi-skill production pipeline with strong character consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to plan and generate short serialized comic-drama episodes while preserving character identity across scripts, turnaround sheets, keyframes, video shots, and local edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote prerequisite installs can pull changed or unreviewed skill versions.

Mitigation: Prefer pinned, reviewed versions of the installer and prerequisite skills, and run installation with minimal permissions.

Risk: Passing an API key through an explicit command-line argument can expose the credential through shell history or process inspection.

Mitigation: Use the prerequisite skills' configured environment variables, typically NANOPHOTO_API_KEY, and reserve explicit --api-key usage for controlled fallback or debugging cases.

Risk: Public asset URLs may expose sensitive or private source material to generation services or downstream viewers.

Mitigation: Use only authorized, non-sensitive public image URLs for turnaround, keyframe, and image-to-video handoffs.

Risk: Generated files and local video edits can clutter or overwrite unrelated workspace data.

Mitigation: Create and use a dedicated project directory for generated documents, downloaded shots, edits, and final exports.

## Reference(s):

- [Comic Drama Generate skill page](https://clawhub.ai/nanophotohq/skills/comic-drama-generate)
- [NanoPhoto AI service homepage](https://nanophoto.ai)
- [NanoPhoto API key management](https://nanophoto.ai/settings/apikeys)
- [End-to-end workflow](artifact/references/workflow.md)
- [Install checklist](artifact/references/install-checklist.md)
- [Asset consistency rules](artifact/references/asset-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown project documents, public asset URLs, local media files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces organized project folders for series notes, episode outlines, shot lists, asset URL tracking, shots, edits, and final exports.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
