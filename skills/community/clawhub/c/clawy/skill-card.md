## Description:

Clawy helps agents create stable mascot avatars and short image-driven adventure arcs using reference-preserving image editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ocean7322](https://clawhub.ai/user/ocean7322)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Clawy to create or refine an agent mascot identity, preserve it across themed scene images, and run lightweight interactive story posts with captions and choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured providers may receive API keys and selected reference or user images when generation is invoked.

Mitigation: Use trusted provider endpoints, avoid custom BASE_URL values unless controlled, and use revocable low-scope API keys with spending limits.

Risk: A missing default mother image may be downloaded from a fallback URL without integrity checks.

Mitigation: Bundle the default image locally or require checksum validation before accepting the fallback download.

Risk: Avatar identity can drift when using unsuitable image generation backends or long image-to-image chains.

Mitigation: Use image-edit or reference-preserving backends and periodically re-anchor from the mother image or a stable character-bearing frame.

## Reference(s):

- [Clawy ClawHub skill page](https://clawhub.ai/ocean7322/skills/clawy)
- [Clawy Asset Rules](references/asset-rules.md)
- [Clawy Image Edit Playbook](references/image-edit-playbook.md)
- [Fallback mother image](https://www.8uddy.land/images/clawy.png)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Images]

**Output Format:** [Markdown with prompts, short captions, choice blocks, shell command examples, and generated image files when a backend is invoked.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write PNG image outputs and may call configured external image-edit providers only when generation is requested.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
