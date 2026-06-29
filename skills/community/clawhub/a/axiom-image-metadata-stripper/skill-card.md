## Description: <br>
Image metadata stripper that removes EXIF, GPS, camera information, and other metadata from JPEG and PNG images using Python standard-library code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and privacy-conscious users use this skill to strip image metadata before publishing or sharing photos that may contain GPS coordinates, camera identifiers, timestamps, or software details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises GIF and directory processing, but the implementation only strips JPEG and PNG files passed as individual file paths. <br>
Mitigation: Use the skill for individual JPEG or PNG files, and verify format support before relying on it for GIFs, directories, or batch workflows. <br>
Risk: The Python usage example shows raw bytes input, while the implemented function accepts file paths and writes an output file. <br>
Mitigation: Call the CLI or pass input and output file paths to the Python function, then inspect the output file before publishing. <br>
Risk: Metadata stripping is all-or-nothing and may not cover unsupported image formats such as WebP, AVIF, or HEIC. <br>
Mitigation: Confirm the input format is supported and use a dedicated metadata inspection tool for formats outside JPEG and PNG. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-image-metadata-stripper) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Source script](artifact/axiom_image_metadata_stripper.py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, Python API examples, generated image files, and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure Python standard-library workflow; writes a stripped image file when run in strip mode and reports detected metadata when run in analyze mode.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
