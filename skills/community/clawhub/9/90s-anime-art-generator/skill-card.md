## Description: <br>
Generate retro 1990s anime and OVA-style illustrations from text prompts through the Neta AI image generation API, with optional output size and reference-image controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate retro anime portraits, scenes, profile images, and related 1990s Japanese animation-style artwork from natural-language prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Neta API token and its documented usage passes that token on the command line. <br>
Mitigation: Use a trusted environment, avoid shared terminals, logs, screenshots, and CI output, and adapt usage to read the token from a protected secret source where possible. <br>
Risk: Prompts and reference identifiers are sent to the external Neta/TalesOfAI image generation service. <br>
Mitigation: Avoid submitting confidential, regulated, or sensitive prompt content unless that external service is approved for the intended use. <br>


## Reference(s): <br>
- [90s Anime Art Generator on ClawHub](https://clawhub.ai/omactiengartelle/90s-anime-art-generator) <br>
- [Neta AI Open](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall output sizes plus an optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
