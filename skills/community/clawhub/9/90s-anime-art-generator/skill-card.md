## Description:

Generate retro 1990s anime and OVA-style illustrations from text prompts, with optional size selection and reference-image style inheritance through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn text prompts into retro Japanese animation style image URLs, with options for portrait, landscape, square, or tall output and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image UUIDs, and API tokens are sent to an external Neta/TalesOfAI service.

Mitigation: Do not submit sensitive or confidential prompts or reference identifiers unless sharing them with that service is acceptable.

Risk: The documented command-line token flow can expose long-lived API tokens in shell history or process listings.

Mitigation: Prefer short-lived or scoped tokens where available, avoid pasting long-lived secrets directly into reusable commands, and rotate tokens if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/90s-anime-art-generator)
- [Neta AI token page](https://www.neta.art/open/)
- [Neta/TalesOfAI image creation endpoint](https://api.talesofai.com/v3/make_image)
- [Neta/TalesOfAI task polling endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, Guidance]

**Output Format:** [Plain text image URL with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; prompt text and optional reference image UUID are sent to the external Neta/TalesOfAI service.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
