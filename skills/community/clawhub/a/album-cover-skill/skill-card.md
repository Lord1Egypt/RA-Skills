## Description: <br>
Generate album cover images from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative agents use this skill to request album cover artwork from a prompt and receive a direct generated image URL for downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference UUIDs, and a Neta API token are sent to api.talesofai.com for image generation. <br>
Mitigation: Use a dedicated or easily rotated Neta token, prefer NETA_TOKEN over command-line secrets, and avoid sensitive or proprietary prompt content. <br>
Risk: The skill depends on an external image generation service and may fail, time out, or return unavailable results. <br>
Mitigation: Handle nonzero exit codes and retry or fall back when the external API does not return a usable image URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/album-cover-skill) <br>
- [Neta API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls] <br>
**Output Format:** [Plain text URL printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token via NETA_TOKEN or --token; supports prompt text, size, style, and optional reference UUID.] <br>

## Skill Version(s): <br>
1.5.7 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
