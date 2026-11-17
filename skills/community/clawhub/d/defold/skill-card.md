## Description:

Develop games using Defold engine with Lua scripting, including components, GUI, physics, animation, input handling, dynamic objects, and save/load systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game builders use this skill for Defold projects that need Lua game code, engine API guidance, GUI and input patterns, physics behavior, animation setup, dynamic object loading, dependency setup, and save/load systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script modifies a game.project file and could add dependencies to the wrong project if run with an unintended path.

Mitigation: Run scripts/add_dependencies.py only against a project file you intend to change and review the diff before opening the project in Defold.

Risk: Recommended GitHub dependencies are URL based and do not include checksums or immutable commit pins.

Mitigation: Review each dependency source and version before adding it; pin or vendor dependencies according to project policy when stronger supply-chain control is required.

Risk: Generic game-development prompts may activate the skill even when the project is not using Defold.

Mitigation: Confirm the project is a Defold/Lua project before applying Defold-specific APIs or dependency changes.

## Reference(s):

- [Core Concepts](references/core-concepts.md)
- [GUI System](references/gui-system.md)
- [Dynamic Objects](references/dynamic-objects.md)
- [Data Storage](references/data-storage.md)
- [Physics System](references/physics-system.md)
- [Animation System](references/animation-system.md)
- [Input System](references/input-system.md)
- [Business Game Patterns](references/business-patterns.md)
- [Defold Manual](https://defold.com/manuals)
- [Druid Framework](https://github.com/Insality/druid)
- [DefSave](https://github.com/subsoap/defsave)
- [Defold Asset Portal](https://defold.com/assets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Lua code examples and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Defold Lua snippets and a user-run dependency helper for game.project files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
