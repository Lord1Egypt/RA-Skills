## Description: <br>
Develop, debug, and upgrade Blender add-ons/plugins and `bpy` scripts with Blender 4.x and 5.x compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Seekerzero](https://clawhub.ai/user/Seekerzero) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create, debug, migrate, and validate Blender add-ons and `bpy` scripts for Blender 4.x and 5.x API compatibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold script can create or replace local add-on files in a user-selected output directory. <br>
Mitigation: Choose the output directory carefully, avoid `--force` unless replacement is intended, and review generated Python before running it in Blender. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Seekerzero/blender-plugin-dev) <br>
- [Blender 4.x to 5.x Compatibility Notes](references/blender4_to_5_compat.md) <br>
- [Blender Script Generation Patterns](references/script_generation_patterns.md) <br>
- [Blender 4.0 Python API release notes](https://developer.blender.org/docs/release_notes/4.0/python_api/) <br>
- [Blender 5.0 Python API release notes](https://developer.blender.org/docs/release_notes/5.0/python_api/) <br>
- [Blender 4.0 API changelog](https://docs.blender.org/api/4.0/change_log.html) <br>
- [Blender 5.0 API changelog](https://docs.blender.org/api/5.0/change_log.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated Python code or files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local Blender add-on scaffold files when the user runs the bundled scaffold script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
