## Description: <br>
Render Aavegotchi assets by deriving renderer hashes from Goldsky Base core data, calling the Aavegotchi renderer batch API, and returning deterministic hashes plus image artifact paths for a token ID or inventory URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to render Aavegotchi assets from a token ID or inventory URL, collect the derived renderer hash, and save returned JSON and PNG artifacts for downstream inspection or workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Node script contacts Goldsky and Aavegotchi with the token or inventory URL supplied by the user. <br>
Mitigation: Run it only when public API access for that token is acceptable and avoid supplying sensitive or private URLs. <br>
Risk: The script writes JSON and PNG artifacts to /tmp by default or to a user-selected output directory. <br>
Mitigation: Choose a non-sensitive output directory and do not run the script with elevated privileges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinnabarhorse/aavegotchi-3d-renderer) <br>
- [Goldsky Base core subgraph endpoint](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn) <br>
- [Aavegotchi renderer batch API](https://www.aavegotchi.com/api/renderer/batch) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, guidance] <br>
**Output Format:** [Text summary with JSON and PNG files saved to disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns token ID, renderer hash, kickoff and verification statuses, poll summary, saved artifact paths, and GLB availability when present.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
