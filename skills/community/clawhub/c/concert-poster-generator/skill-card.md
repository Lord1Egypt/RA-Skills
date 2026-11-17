## Description:

Generate bold concert posters, gig flyers, music event banners, band promo art, festival posters, club night flyers, and live show announcement designs from a text prompt via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, musicians, DJs, venue promoters, and tour managers use this skill to generate concert posters, gig flyers, festival banners, club night artwork, and live show announcement designs from short prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Neta API token and accepts it on the command line, where it may be exposed through shell history or process inspection.

Mitigation: Use a dedicated low-privilege Neta token and rotate it if it was pasted into shell history, logs, or shared terminals.

Risk: Prompts, reference IDs, and the token are sent to api.talesofai.com for image generation.

Mitigation: Avoid submitting confidential prompts or sensitive reference identifiers unless the external service is approved for that data.

Risk: The security verdict is suspicious because the token handling and external-service disclosure need review before installation.

Mitigation: Review the skill before deployment and prefer a version-pinned or trusted installer path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/concert-poster-generator)
- [Neta API token setup](https://www.neta.art/open/)
- [Neta image generation API endpoint](https://api.talesofai.com/v3/make_image)
- [Neta image task polling endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script sends the prompt, optional reference image ID, canvas size, and Neta token to api.talesofai.com, then polls for a generated image URL.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
