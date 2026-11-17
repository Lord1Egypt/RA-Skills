## Description:

Engine configuration wizard for Godot 4.6, Unity 7, and UE 5.6 that handles project creation, version control, renderer settings, and platform-specific setup with version-aware references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toilanguyen2910](https://clawhub.ai/user/toilanguyen2910)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game teams use this skill to configure new Godot, Unity, or Unreal Engine projects, select renderer and platform settings, set up version control, and verify a starter build or scene.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers could activate the skill for a generic project setup request.

Mitigation: Use the skill when the user specifically wants game engine project setup.

Risk: The skill can propose project-file edits, git initialization, and engine build commands.

Mitigation: Review prompts and generated changes before allowing file creation, git initialization, or build commands.

## Reference(s):

- [Game Dev setup-engine on ClawHub](https://clawhub.ai/toilanguyen2910/skills/game-dev-setup-engine)
- [Godot gitignore](https://github.com/github/gitignore/blob/main/Godot.gitignore)
- [Unity gitignore](https://github.com/github/gitignore/blob/main/Unity.gitignore)
- [Unreal Engine gitignore](https://github.com/github/gitignore/blob/main/UnrealEngine.gitignore)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project files, folder structures, git setup, and engine CLI verification steps for user review.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
