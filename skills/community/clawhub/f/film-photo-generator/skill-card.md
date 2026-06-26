## Description: <br>
Generate authentic analog-style film photographs with 35mm grain, light leaks, and faded retro color palettes for nostalgic portraits, vintage 70s/80s aesthetic photos, Instagram film looks, Kodak Portra style imagery, lomography effects, Fujifilm simulation, and retro mood boards via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, developers, and agents use this skill to generate analog-style film photo outputs from text prompts, with optional image-reference style inheritance and size selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image IDs, and the API token are sent to the Neta/TalesOfAI service. <br>
Mitigation: Avoid confidential or regulated prompts and reference images, and use the skill only when the remote service is acceptable for the intended data. <br>
Risk: Passing the API token on the command line can expose it through shell history or process listings. <br>
Mitigation: Use a dedicated, revocable token and avoid reusing privileged credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/omactiengartelle/film-photo-generator) <br>
- [Neta API token page](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill submits a remote image-generation job, polls for completion, and returns one direct image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
