## Description: <br>
Query Atlas Obscura places for weird/obscure location inspiration. Use when you need nearby curiosities by coordinates, place lookup by ID, or global place coordinates for creative prompt spice and worldbuilding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougbtv](https://clawhub.ai/user/dougbtv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creative technologists, and agents use this skill to fetch Atlas Obscura place data for nearby curiosities, place lookups, and location-inspired worldbuilding context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper installs third-party npm packages. <br>
Mitigation: Install in a disposable project or container when operating under stricter dependency controls. <br>
Risk: User-supplied coordinates or place IDs are sent through the Atlas Obscura API library. <br>
Mitigation: Avoid submitting sensitive locations or identifiers unless that sharing is acceptable for the workflow. <br>
Risk: Atlas Obscura site or library behavior may drift and return partial or missing fields. <br>
Mitigation: Return partial data with clear notes about field gaps and rerun with broader or alternate inputs when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dougbtv/atlas-obscura-api) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/dougbtv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper returns JSON for search results, place details, and place coordinate samples.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
