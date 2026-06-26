## Description: <br>
Generates D&D character art images from text descriptions via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request fantasy D&D character portraits from prompts, optionally controlling image size or using a reference image for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference IDs, and a Neta/TalesOfAI API token are sent to an external image service. <br>
Mitigation: Use a token scoped to this provider and avoid sending secrets or sensitive campaign material in prompts. <br>
Risk: Typing API tokens directly into commands can leave reusable secrets in shell history. <br>
Mitigation: Pass the token through a shell variable or another secret-handling mechanism instead of typing it directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/dnd-character-skill) <br>
- [Neta AI token setup](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text image URL with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference image UUID affect generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
