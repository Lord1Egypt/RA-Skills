## Description: <br>
Quick product image processing that adds a price sticker, watermark, and logo when the user sends `$price:` with an image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rueshady](https://clawhub.ai/user/rueshady) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, creators, and storefront operators use this skill to turn product photos into listing-ready images by adding a price sticker, optional watermark, and logo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup helper can make package-manager changes when run with installation enabled. <br>
Mitigation: Run `setup.sh --install` only on machines where package changes are acceptable, or install ImageMagick, bc, and python3 manually. <br>
Risk: The latest-image mode can process an unintended file if the incoming image folder is too broad. <br>
Mitigation: Keep the incoming image directory scoped to product photos intended for processing, and set `ECDYSALES_MEDIA_DIR` when needed. <br>
Risk: Generated outputs may accumulate in the output directory. <br>
Mitigation: Review outputs before use and clean the output directory periodically to avoid unnecessary disk growth. <br>


## Reference(s): <br>
- [Ecdysales on ClawHub](https://clawhub.ai/rueshady/ecdysales) <br>
- [HOWTO.md](HOWTO.md) <br>
- [ImageMagick](https://imagemagick.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Processed image file with command output path; JSON output is available in CLI mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ImageMagick processing and writes generated images to an output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
