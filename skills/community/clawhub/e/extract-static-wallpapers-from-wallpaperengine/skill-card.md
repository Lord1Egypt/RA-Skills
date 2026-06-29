## Description: <br>
Extracts static PNG wallpapers and mipmap resolutions from Wallpaper Engine scene.pkg files in PKGV0023/PKGV0024 format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pandhumhp-cn](https://clawhub.ai/user/pandhumhp-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced users use this skill to recover static wallpaper images from trusted Wallpaper Engine scene.pkg packages, including embedded PNGs in .tex textures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted scene.pkg can use package-controlled paths to write outside the intended output directory. <br>
Mitigation: Run only on trusted packages in a temporary or sandboxed directory with an explicit output path; review the extractor to reject absolute paths and '..' segments, cap entry sizes, validate offsets, and allowlist expected wallpaper file types. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pandhumhp-cn/extract-static-wallpapers-from-wallpaperengine) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, files] <br>
**Output Format:** [Markdown guidance with shell commands and extracted PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extracted package contents and wallpaper PNG files when run on a local scene.pkg input.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
