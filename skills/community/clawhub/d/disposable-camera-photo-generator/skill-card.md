## Description:

Generates disposable-camera-style photos from text prompts using the Neta AI image generation API, with options for output size and reference-image style inheritance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate stylized disposable-camera images from text prompts. The skill supports square, portrait, landscape, and tall outputs, plus optional reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Neta API token is supplied on the command line, which can expose it through shell history or local process inspection.

Mitigation: Use a dedicated low-scope token, avoid shared shells, and rotate the token if it may have been exposed.

Risk: The documented npx install path is mutable and may not always resolve to the same reviewed artifact.

Mitigation: Prefer a trusted or pinned install path when available, and review the installed files before execution.

Risk: Prompts and reference image identifiers are sent to an external image-generation service.

Mitigation: Do not submit sensitive prompts or reference IDs unless external processing by that service is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blammectrappora/skills/disposable-camera-photo-generator)
- [Neta API access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text image URL returned after command-line execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status and polling messages are written to stderr; the generated image URL is written to stdout.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
