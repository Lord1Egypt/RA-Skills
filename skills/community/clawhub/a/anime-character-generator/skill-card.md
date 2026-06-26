## Description: <br>
Generate full-body anime characters with custom outfits, hairstyles, and poses via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to generate anime-style character image URLs from text prompts for original characters, fan art, avatars, and visual novel assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and Neta API tokens are sent to an external image generation API. <br>
Mitigation: Use a dedicated or revocable token, avoid sensitive prompts or proprietary reference identifiers, and pass secrets through an environment variable or other secret-safe workflow. <br>


## Reference(s): <br>
- [Anime Character Generator on ClawHub](https://clawhub.ai/omactiengartelle/anime-character-generator) <br>
- [Neta API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference UUID flags influence the generated image.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
