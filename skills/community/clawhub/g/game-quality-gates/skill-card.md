## Description:

Game development quality gates and mandatory checks for building, reviewing, debugging, or deploying H5, Canvas, WebGL, Phaser, Three.js, 2D, and 3D game projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abczsl520](https://clawhub.ai/user/abczsl520)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill as a pre-deploy and diagnostic checklist for game projects, especially to catch lifecycle, cleanup, input, audio, persistence, networking, anti-cheat, asset loading, and performance issues. It provides universal game quality gates plus Phaser, Three.js, and web-game anti-cheat guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-trigger across a broad range of game-development work and may surface checklist items outside the immediate project context.

Mitigation: Review the recommendations against the game engine, platform, and release stage before applying them.

Risk: Three.js asset-compression examples use npx commands that may fetch package code at execution time.

Mitigation: Pin @gltf-transform/cli to a reviewed version or run an already installed local binary under a lockfile.

Risk: Manual clone or update installation depends on the integrity of external source content.

Mitigation: Review the source and release evidence before manual git clone or git pull installs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abczsl520/skills/game-quality-gates)
- [Universal Rules](docs/Universal-Rules.md)
- [Phaser Guide](references/phaser.md)
- [Three.js Guide](references/threejs.md)
- [Anti-Cheat Patterns](references/anti-cheat.md)
- [Game Quality Gates Wiki](https://github.com/abczsl520/game-quality-gates/wiki)
- [Phaser Wiki Guide](https://github.com/abczsl520/game-quality-gates/wiki/Phaser-Guide)
- [Three.js Wiki Guide](https://github.com/abczsl520/game-quality-gates/wiki/Threejs-Guide)
- [Anti-Cheat Wiki Patterns](https://github.com/abczsl520/game-quality-gates/wiki/Anti-Cheat-Patterns)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, code examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Engine-specific references are loaded when Phaser, Three.js, or anti-cheat guidance is relevant.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
