## Description: <br>
Create 3D anime posters with volumetric lighting, cinematic depth, dynamic compositions, and optional reference-image style inheritance through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate anime-style poster image URLs from text prompts, with size selection and optional reference-image UUIDs for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Avoid confidential prompts or sensitive reference identifiers, and use the skill only when that third-party API disclosure is acceptable. <br>
Risk: Passing tokens on the command line can expose them on shared machines through process listings or shell history. <br>
Mitigation: Use this skill on trusted machines and avoid command-line token usage where local process arguments or shell history may be visible to others. <br>


## Reference(s): <br>
- [Neta API token and trial page](https://www.neta.art/open/) <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/3d-anime-poster-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, Guidance] <br>
**Output Format:** [Command-line text output containing a direct image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; sends the prompt and optional reference image UUID to the Neta/TalesOfAI service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
