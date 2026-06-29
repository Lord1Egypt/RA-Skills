## Description: <br>
Converts JPG or PNG images into round Android app icon PNGs across mdpi, hdpi, xhdpi, xxhdpi, and xxxhdpi densities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starclimber](https://clawhub.ai/user/starclimber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and app builders use this skill to turn a supplied JPG or PNG into Android launcher icon assets with round cropping and standard density variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad icon-related trigger phrases may invoke this skill when a different image task was intended. <br>
Mitigation: Confirm the user wants Android app icon generation before running the icon conversion workflow. <br>
Risk: Generated icons could be copied into the wrong Android project or replace existing launcher assets. <br>
Mitigation: Ask the user which project or output directory to use, and review generated files before copying them into mipmap directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/starclimber/skills/androidiconmaker) <br>
- [Publisher profile](https://clawhub.ai/user/starclimber) <br>
- [Project repository link from README](https://github.com/starclimber/android-icon-maker) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [Markdown guidance plus generated PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates icon_mdpi.png, icon_hdpi.png, icon_xhdpi.png, icon_xxhdpi.png, and icon_xxxhdpi.png; default mdpi base size is 48 px.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
