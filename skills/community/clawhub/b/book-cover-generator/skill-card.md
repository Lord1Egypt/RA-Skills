## Description:

AI book cover generator for indie authors and self-publishers that creates KDP book covers, novel cover art, ebook covers, and Kindle cover designs using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, self-publishers, and KDP creators use this skill to generate genre-specific book cover image URLs from text descriptions. The skill supports portrait, landscape, square, and tall dimensions and can optionally inherit style from a reference image UUID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an API token for an external image service.

Mitigation: Use a disposable or least-privileged Neta API token and avoid passing long-lived secrets directly in shell commands.

Risk: Prompts and optional reference identifiers are transmitted to the external image provider.

Mitigation: Do not submit confidential manuscript material, unreleased cover concepts, or sensitive reference assets unless that transmission is acceptable.

Risk: The server security summary flags the release as suspicious because provider and credential-handling risks are under-disclosed.

Mitigation: Review the skill before installing and prefer a pinned or ClawHub-verified install path over an unpinned npx command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/book-cover-generator)
- [Neta AI token signup](https://www.neta.art/open/)
- [Neta image generation API endpoint](https://api.talesofai.com/v3/make_image)
- [Neta image task status API endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text image URL with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token supplied with --token; sends prompts and optional reference UUIDs to an external image generation service.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
