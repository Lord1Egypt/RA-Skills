## Description: <br>
AI fantasy map generator for worldbuilders, tabletop RPG campaigns, and game designers. Create custom fantasy world maps, dungeon maps, kingdom maps, and lore art - perfect for D&D, Pathfinder, and indie game development via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, tabletop RPG players, worldbuilders, and game developers use this skill to generate fantasy world, dungeon, kingdom, and lore-map image URLs from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and the Neta API token are sent to api.talesofai.com. <br>
Mitigation: Treat the token like a password, prefer passing it from an environment variable, and avoid private, regulated, or proprietary prompt content unless the provider is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/fantasy-map-generator) <br>
- [Neta Open](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [Plain text image URL printed to stdout, with status and errors printed to stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token and sends prompts to api.talesofai.com for image generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
