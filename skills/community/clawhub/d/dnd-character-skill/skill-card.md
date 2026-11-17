## Description:

Generate D&D character art from text descriptions via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate fantasy role-playing character artwork from text prompts, with optional image size and reference-style settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, reference IDs, and a Neta token to an external API.

Mitigation: Use only a token intended for api.talesofai.com and avoid private, sensitive, or regulated content in prompts and reference IDs.

Risk: The README includes an unpinned npx install command.

Mitigation: Prefer a pinned version or a ClawHub-managed install path when installing in production environments.

Risk: Image generation can fail, time out, or be held by service moderation.

Mitigation: Handle missing URLs, API failures, and timeouts before relying on generated images in an automated workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/dnd-character-skill)
- [Neta token setup](https://www.neta.art/open/)
- [Neta image creation API endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with Markdown shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall image sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
