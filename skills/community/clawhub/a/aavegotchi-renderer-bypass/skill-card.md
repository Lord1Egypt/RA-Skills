## Description:

Render Aavegotchi assets by deriving renderer hashes from Goldsky Base core data and calling POST /api/renderer/batch on www.aavegotchi.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to render Aavegotchi image and 3D asset availability artifacts from a tokenId or inventory URL. It is intended for deterministic renderer hash derivation, renderer batch API execution, and saving returned JSON and PNG outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound calls to Goldsky and Aavegotchi endpoints.

Mitigation: Use it only in environments where those outbound calls are expected and approved.

Risk: Renderer-supplied image URLs may be fetched during artifact download.

Mitigation: Review network behavior before installation and prefer domain allowlisting for image downloads.

Risk: The helper writes predictable artifact filenames to /tmp by default.

Mitigation: Run as an unprivileged user and set a private output directory with --out-dir.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinnabarhorse/skills/aavegotchi-renderer-bypass)
- [Goldsky Aavegotchi Core Base subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn)
- [Aavegotchi renderer batch API](https://www.aavegotchi.com/api/renderer/batch)
- [Aavegotchi web application](https://www.aavegotchi.com)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus JSON and PNG file artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns tokenId, renderer hash, HTTP statuses, saved artifact paths, and GLB availability when present.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
