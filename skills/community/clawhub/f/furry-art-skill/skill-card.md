## Description:

Generate furry art images from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate furry art images from text prompts, optionally selecting image size or referencing an existing image for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles the Neta/Tales of AI token through command-line arguments, which can expose secrets in shell history, logs, or process telemetry.

Mitigation: Pass tokens through protected environment handling where possible, avoid placing real tokens directly on command lines, and rotate any token that may already have been exposed.

Risk: The install instructions use mutable package installation paths, so a future install may not resolve to the reviewed release.

Mitigation: Prefer a version-pinned install path or verify the installed artifact hash against the reviewed release before use.

Risk: Prompts and API tokens are sent to api.talesofai.com for image generation.

Mitigation: Install and run only when that external service interaction is acceptable for the prompts, tokens, and usage environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/furry-art-skill)
- [Neta AI token and API access](https://www.neta.art/open/)
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image)
- [Neta task polling endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands; the runtime script prints an image URL to stdout and progress or errors to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and network access to api.talesofai.com; supports square, portrait, landscape, and tall image sizes.]

## Skill Version(s):

1.6.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
