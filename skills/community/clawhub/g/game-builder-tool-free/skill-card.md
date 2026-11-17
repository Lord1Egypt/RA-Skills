## Description:

Generates playable browser-based 3D mini-games from natural-language Chinese prompts, with iterative edits and local preview support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, game hobbyists, and creative prototypers use this skill to turn Chinese natural-language game concepts into browser-playable Three.js prototypes, then iterate on mechanics, controls, HUDs, and local preview behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security summary flags unsupported temporary sharing-link claims.

Mitigation: Use the skill for local browser preview only unless the publisher documents where shared files are hosted, who can access them, and how links expire.

Risk: The ClawHub security guidance says the trigger wording is broader than the skill's actual 3D game prototyping purpose.

Mitigation: Narrow activation to local browser 3D game generation, Three.js learning prototypes, and iterative mini-game edits.

Risk: The artifact can produce shell commands and local files during preview workflows.

Mitigation: Review commands before execution, avoid passing untrusted user input into shell commands, and inspect generated HTML before reuse or publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/game-builder-tool-free)
- [Three.js 0.160.0 module CDN](https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js)
- [Three.js 0.160.0 addon CDN](https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, and shell command blocks; generated game output is usually a single self-contained HTML file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files such as index.html and progress.md and preview them through a local browser server; generated games load Three.js from jsDelivr CDN.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
