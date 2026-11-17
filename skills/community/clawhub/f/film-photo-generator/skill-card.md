## Description:

Generates analog-style film photographs from text prompts with 35mm grain, light leaks, and retro color palettes via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate retro analog-style images from text prompts, optionally selecting an orientation or passing a reference image UUID for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional reference image IDs are sent to an external Neta/TalesOfAI service.

Mitigation: Use only prompts and reference IDs that are acceptable to share with that service.

Risk: The API token is passed with a command-line flag, which can expose it in shell history or process listings on shared or logged systems.

Mitigation: Avoid entering real tokens directly in logged or shared shell sessions; prefer an approved secret-handling workflow when available.

Risk: The security scan verdict is suspicious because external data sharing and token handling are under-disclosed.

Mitigation: Review the skill and security guidance before installation, and prefer a pinned or ClawHub-managed install path.

## Reference(s):

- [Film Photo Generator on ClawHub](https://clawhub.ai/omactiengartelle/skills/film-photo-generator)
- [Publisher profile: omactiengartelle](https://clawhub.ai/user/omactiengartelle)
- [Neta API access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text direct image URL, with Markdown usage examples in the documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token and sends prompts, optional reference IDs, and size choices to the Neta/TalesOfAI service.]

## Skill Version(s):

1.0.0 (source: evidence release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
