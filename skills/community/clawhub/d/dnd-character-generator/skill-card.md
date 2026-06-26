## Description: <br>
Generate cinematic D&D character portraits and tabletop RPG hero art from a text description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, players, dungeon masters, and tabletop RPG creators use this skill to generate character portrait prompts through the Neta image generation service and receive an image URL for campaign or virtual tabletop use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, optional reference IDs, and the API token are sent to an external image-generation service. <br>
Mitigation: Use only trusted Neta/TalesOfAI tokens, avoid submitting confidential campaign or personal data, and prefer limited tokens. <br>
Risk: Passing the API token with --token may leave local command-line traces. <br>
Mitigation: Run the command in a controlled environment and avoid sharing shell history or process listings that may expose the token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/dnd-character-generator) <br>
- [Neta API token portal](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and sends prompts, optional reference image UUIDs, and generation settings to the disclosed external image-generation service.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
