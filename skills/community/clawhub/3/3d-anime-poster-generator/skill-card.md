## Description:

Generates 3D anime poster images from text prompts using the Neta AI image generation API, with size options and optional reference image style inheritance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, designers, and developers use this skill to generate anime-style poster image URLs from text prompts for wallpapers, merchandise concepts, fan art, print-on-demand art, and decorative designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts, optional reference image UUIDs, and the Neta API token are sent to api.talesofai.com.

Mitigation: Use the skill only with prompts and references you are comfortable sending to that third-party service.

Risk: Passing a long-lived token on the command line can expose it through shell history or process inspection.

Mitigation: Prefer short-lived or revokable tokens when available, avoid reusing sensitive tokens, and clear command history after use.

Risk: Generated image URLs and content depend on the third-party API, its moderation, and its availability.

Mitigation: Review generated outputs before reuse and plan for retry or fallback behavior when the API fails or times out.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/3d-anime-poster-generator)
- [Neta API token access](https://www.neta.art/open/)
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints a direct generated image URL after polling the Neta API.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
