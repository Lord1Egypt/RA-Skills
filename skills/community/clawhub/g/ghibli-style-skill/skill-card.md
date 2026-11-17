## Description:

Generate studio ghibli ai art generator images with AI via the Neta AI image generation API (free trial at neta.art/open).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wkl-nieta](https://clawhub.ai/user/wkl-nieta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate AI images from text prompts through the Neta image generation API and receive a direct image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and an API token to an external image generation service.

Mitigation: Use only prompts and account credentials appropriate for that provider, and verify the provider relationship between Neta and api.talesofai.com before use.

Risk: The script accepts the API token through a command-line flag, which can expose credentials in local shell history or process listings.

Mitigation: Avoid placing real tokens directly on the command line; use a controlled environment variable flow or wrapper that does not persist the token.

Risk: The runtime API destination is not consistently disclosed across skill metadata.

Mitigation: Review the documented endpoints and pin the installed skill version before using a real account token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wkl-nieta/skills/ghibli-style-skill)
- [Neta API token signup](https://www.neta.art/open/)
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image)
- [Neta image task polling endpoint](https://api.talesofai.com/v1/artifact/task/${task_uuid})

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration]

**Output Format:** [Plain text image URL with command-line status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and accepts prompt, size, style, and optional reference image parameters.]

## Skill Version(s):

2.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
