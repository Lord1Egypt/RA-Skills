## Description: <br>
Generate furry art generator ai images with AI via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request furry-style image generation from text prompts through the Neta/TalesOfAI API and receive a generated image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta/TalesOfAI API token are sent to api.talesofai.com. <br>
Mitigation: Use restricted or short-lived tokens, avoid sensitive prompts, and avoid exposing long-lived tokens in shell history or shared terminal logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/furry-art-skill) <br>
- [Neta AI API access](https://www.neta.art/open/) <br>
- [Neta/TalesOfAI image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, Guidance] <br>
**Output Format:** [Plain text URL with progress messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and sends the prompt, optional reference image UUID, and token to api.talesofai.com.] <br>

## Skill Version(s): <br>
1.6.4 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
