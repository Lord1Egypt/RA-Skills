## Description: <br>
Work with OpenEXR files to inspect channels, extract beauty/RGB passes, decode cryptomatte segmentation, convert ACEScg to sRGB, and batch process EXR directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oumad](https://clawhub.ai/user/oumad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical artists use this skill to inspect and process OpenEXR render files, extract PNG previews or segmentation masks, and prepare render outputs for review, compositing, or dataset workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-selected EXR files and writes derived PNG outputs, and --force can overwrite existing generated files. <br>
Mitigation: Install and run it in a virtual environment, use it on trusted or reviewed EXR inputs, and use --force only when overwriting outputs is intended. <br>
Risk: The OpenEXR dependency is pinned because later versions are documented as unstable on some platforms. <br>
Mitigation: Install dependencies from requirements.txt, keep OpenEXR pinned to 3.2.4 for this release, and audit or pin transitive dependencies before production deployment. <br>


## Reference(s): <br>
- [ClawHub OpenEXR Skill Page](https://clawhub.ai/oumad/exr) <br>
- [Usage Examples](references/usage.md) <br>
- [Color Space Reference](references/color-spaces.md) <br>
- [Cryptomatte Format Reference](references/cryptomatte.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline bash and Python snippets; PNG image files when the bundled CLI is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI reads selected EXR files or directories and writes derived PNG outputs; existing outputs are skipped unless --force is used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
