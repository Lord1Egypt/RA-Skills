## Description: <br>
Generates cosplay reference sheets and costume design illustrations from character or outfit descriptions using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, cosplayers, commissioners, sellers, and tutorial authors use this skill to turn costume or character descriptions into full-body cosplay reference imagery for planning, listings, and visual direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta API token are sent to an external image-generation service. <br>
Mitigation: Use a fresh or low-privilege token, avoid sensitive or confidential prompts, and rotate the token if it may have appeared in shell history, logs, or shared screenshots. <br>
Risk: The skill returns generated image URLs from a third-party service, so availability and output quality depend on that service. <br>
Mitigation: Review generated outputs before using them in production materials and keep a fallback workflow for service failures or unsuitable results. <br>


## Reference(s): <br>
- [Neta AI token signup](https://www.neta.art/open/) <br>
- [Cosplay Reference Generator on ClawHub](https://clawhub.ai/blammectrappora/cosplay-reference-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Direct image URL printed as a string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference image UUID affect the generated image.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
