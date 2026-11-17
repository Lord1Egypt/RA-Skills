## Description:

Render Aavegotchi assets by deriving renderer hashes from Goldsky Base core data and calling POST /api/renderer/batch on www.aavegotchi.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinnabarhorse](https://clawhub.ai/user/cinnabarhorse)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to render Aavegotchi token assets from a token ID or inventory URL, producing a deterministic renderer hash plus image and availability artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script may fetch renderer-provided download URLs too broadly, which could cause arbitrary or oversized remote content to be downloaded.

Mitigation: Use the skill only where outbound network requests are acceptable, avoid hosts with sensitive internal HTTP services, and prefer a restricted output directory.

Risk: The security guidance says the skill would be safer with stricter artifact URL validation, request timeouts, and download size limits.

Mitigation: Review before installing and validate artifact URLs against expected Aavegotchi or CDN hosts before using the downloaded outputs.

## Reference(s):

- [Goldsky Base Core Subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn)
- [Aavegotchi Renderer Batch API](https://www.aavegotchi.com/api/renderer/batch)
- [Aavegotchi](https://www.aavegotchi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with shell commands and JSON or image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a renderer hash, HTTP statuses, raw batch JSON paths, poll summary, PNG artifact paths when available, and GLB availability information.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
