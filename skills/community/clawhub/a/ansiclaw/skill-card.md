## Description:

Draws BBS compatible ANSI art via the Clawbius API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n2tr0n](https://clawhub.ai/user/n2tr0n)

### License/Terms of Use:


## Use Case:

Developers, artists, and external users use ANSIClaw to create BBS-compatible ANSI artwork by scripting against a local Clawbius API, including image-inspired ANSI renditions when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can write fixed output filenames under Desktop or Documents, which may overwrite prior ANSI or PNG files.

Mitigation: Confirm output paths before running and change scripts to save into the skill output folder with versioned filenames.

Risk: Opening reference ANSI files in Clawbius makes them the active canvas, so subsequent draw calls could alter source material.

Mitigation: Analyze reference files read-only and immediately create a new canvas before drawing.

Risk: The skill depends on a local Clawbius API, and stale endpoint assumptions can cause failed or unintended operations.

Mitigation: Confirm the local service is running and refresh the OpenAPI document at session start.

## Reference(s):

- [ClawHub ANSIClaw skill page](https://clawhub.ai/n2tr0n/skills/ansiclaw)
- [n2tr0n publisher profile](https://clawhub.ai/user/n2tr0n)
- [Clawbius API Reference](references/api.md)
- [Clawbius dependency](https://github.com/n2tr0n/clawbius)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell snippets; generated ANSI and PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Clawbius service on 127.0.0.1:7777; generated example scripts may save fixed filenames unless changed.]

## Skill Version(s):

0.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
