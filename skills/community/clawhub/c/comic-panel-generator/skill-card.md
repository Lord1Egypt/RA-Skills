## Description: <br>
Generates AI comic book panels, manga strips, and graphic novel art from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create comic-panel, manga, webcomic, storyboard, and graphic-novel style images from text prompts, with optional size and reference-image controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference image UUIDs, and the Neta token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Avoid secrets, private business data, and sensitive personal information in prompts, and rotate the token if it is exposed. <br>


## Reference(s): <br>
- [Comic Panel Generator on ClawHub](https://clawhub.ai/blammectrappora/comic-panel-generator) <br>
- [Neta AI token and free trial](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text URL with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a direct image URL after polling the Neta/TalesOfAI service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
