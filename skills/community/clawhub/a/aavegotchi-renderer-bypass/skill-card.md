## Description: <br>
Render Aavegotchi assets by deriving renderer hashes from Goldsky Base core data and calling POST /api/renderer/batch on www.aavegotchi.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Aavegotchi users use this skill to render public Aavegotchi token assets, derive the renderer hash, and save JSON and PNG artifacts from supported renderer responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Node script contacts Goldsky and Aavegotchi and writes JSON and PNG artifacts to disk. <br>
Mitigation: Use public token IDs, choose a dedicated output directory, and review generated files before sharing or reusing them. <br>
Risk: An untrusted output directory could place generated artifacts in a shared or sensitive location. <br>
Mitigation: Avoid accepting --out-dir values from untrusted input and prefer a controlled temporary or project-specific output directory. <br>


## Reference(s): <br>
- [Aavegotchi Renderer Bypass on ClawHub](https://clawhub.ai/cinnabarhorse/aavegotchi-renderer-bypass) <br>
- [Goldsky Aavegotchi Core Base Subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn) <br>
- [Aavegotchi Renderer Batch API](https://www.aavegotchi.com/api/renderer/batch) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON summaries, and saved JSON/PNG artifact paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns token ID, derived hash, API status, raw response path, image artifact paths when available, and GLB availability.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
