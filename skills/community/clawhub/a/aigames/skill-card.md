## Description: <br>
Guides agents through creating mobile-compatible H5 game files and uploading config, game code, and preview assets to the idlab.top game publishing service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianclan](https://clawhub.ai/user/brianclan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to package a small HTML game with its configuration and preview image, then publish those files through the documented upload endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uploads local game files to an external publishing service where they may become public. <br>
Mitigation: Confirm the destination, folder name, and exact files before running upload commands, and do not upload secrets, private documents, system files, or non-public content. <br>
Risk: The documented endpoints do not overwrite existing files, and overwrite behavior can replace previously published content when using a general interface. <br>
Mitigation: Check whether the target folder already exists and keep a backup or versioned replacement plan before attempting any overwrite workflow. <br>


## Reference(s): <br>
- [Aigames Skill Page](https://clawhub.ai/brianclan/aigames) <br>
- [idlab.top Game Upload Service](https://www.idlab.top) <br>
- [thenext.games Game URL Pattern](https://thenext.games/game/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with JSON examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces upload steps for config.json, index.html, and preview.png; individual uploaded files are described as limited to 50MB.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
