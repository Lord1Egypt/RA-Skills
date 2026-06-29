## Description: <br>
Engine configuration wizard for Godot 4.6, Unity 7, and UE 5.6 that handles project creation, version control, renderer settings, and platform-specific setup with version-aware references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toilanguyen2910](https://clawhub.ai/user/toilanguyen2910) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and game teams use this skill to configure new Godot, Unity, or Unreal Engine projects, choose engine-specific settings, create project structure, set up version control, and verify a basic build or scene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad project-initialization phrasing and propose actions before the intended engine or workspace is clear. <br>
Mitigation: Confirm the engine, project directory, and user intent before allowing file writes, git initialization, or build commands. <br>
Risk: Generated configuration files, git setup, or engine CLI commands can modify an existing project if applied in the wrong directory. <br>
Mitigation: Review proposed file paths and commands, use a clean project folder when possible, and inspect generated files before relying on them. <br>


## Reference(s): <br>
- [Godot gitignore template](https://github.com/github/gitignore/blob/main/Godot.gitignore) <br>
- [Unity gitignore template](https://github.com/github/gitignore/blob/main/Unity.gitignore) <br>
- [Unreal Engine gitignore template](https://github.com/github/gitignore/blob/main/UnrealEngine.gitignore) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose project files, configuration snippets, git setup, and engine build commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
